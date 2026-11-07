# MLflow's own Python client driven against Myna's tracking server, and what
# it reads back checked: experiments, runs, params, metrics and their
# history, tags, search, artifacts, a logged scikit-learn model, the model
# registry (versions, aliases, stages, tags) and deletes.
#
#   crow run main.co        (Myna on its port, MYNA_DATA a scratch workspace)
#   ~/.venvs/mlflow/bin/python tests/mlflow/client_check.py http://127.0.0.1:3800
#
# It makes its experiments under a name of its own (client-check-<time>), and
# exits non-zero if any check fails.
import sys, os, time, json, warnings
warnings.filterwarnings('ignore')
os.environ['MLFLOW_DISABLE_AGENT_HINT'] = '1'
import mlflow, numpy as np, pandas as pd
from mlflow import MlflowClient
from sklearn.linear_model import LinearRegression
uri = sys.argv[1]
mlflow.set_tracking_uri(uri)
client = MlflowClient()
results = []
def check(name, ok, note=''):
    results.append((name, bool(ok)))
    print(('ok  ' if ok else 'FAIL') + ' ' + name + ((' — ' + str(note)) if (note is not None and not isinstance(note, str) or note) and not ok else ''), flush=True)

tag = str(int(time.time()))
exp_name = 'client-check-' + tag
exp = mlflow.set_experiment(exp_name)
check('experiment made', exp.name == exp_name and exp.experiment_id)
X = np.array([[1.0], [2.0], [3.0], [4.0]]); y = np.array([2.0, 4.1, 5.9, 8.2])
with mlflow.start_run(run_name='first') as run:
    rid = run.info.run_id
    mlflow.log_param('alpha', 0.5)
    mlflow.log_params({'layers': 3, 'kind': 'linear'})
    for step in range(5):
        mlflow.log_metric('loss', 1.0 / (step + 1), step=step)
    mlflow.log_metrics({'rmse': 0.25, 'r2': 0.97})
    mlflow.set_tag('team', 'lab')
    mlflow.set_tags({'stage': 'try'})
    mlflow.log_text('hello', 'notes/hello.txt')
    mlflow.log_dict({'a': 1}, 'config.json')
    df = pd.DataFrame({'x': [1.0, 2.0], 'y': [2.0, 4.0]})
    mlflow.log_input(mlflow.data.from_pandas(df, name='train'), context='training')
    model = LinearRegression().fit(X, y)
    info = mlflow.sklearn.log_model(model, name='model', registered_model_name='check-model-' + tag, input_example=X[:2])
    with mlflow.start_run(run_name='child', nested=True) as child:
        mlflow.log_metric('loss', 0.1)
        child_id = child.info.run_id
got = client.get_run(rid)
check('params read back', got.data.params == {'alpha': '0.5', 'layers': '3', 'kind': 'linear'}, got.data.params)
check('latest metrics', got.data.metrics.get('loss') == 0.2 and got.data.metrics.get('rmse') == 0.25, got.data.metrics)
check('tags read back', got.data.tags.get('team') == 'lab' and got.data.tags.get('stage') == 'try', got.data.tags)
check('run finished', got.info.status == 'FINISHED' and got.info.end_time, got.info)
hist = client.get_metric_history(rid, 'loss')
check('metric history', [m.step for m in hist] == [0, 1, 2, 3, 4], [(m.step, m.value) for m in hist])
arts = [a.path for a in client.list_artifacts(rid)]
check('artifacts listed', 'config.json' in arts and 'notes' in arts, arts)
check('child run nested', client.get_run(child_id).data.tags.get('mlflow.parentRunId') == rid)
check('dataset input', len(got.inputs.dataset_inputs) == 1 and got.inputs.dataset_inputs[0].dataset.name == 'train', got.inputs)
found = mlflow.search_runs(experiment_ids=[exp.experiment_id], filter_string="metrics.rmse < 1 and params.alpha = '0.5'", order_by=['metrics.rmse ASC'])
check('search runs', len(found) == 1 and found['run_id'][0] == rid, len(found))
found2 = mlflow.search_runs(experiment_ids=[exp.experiment_id], filter_string="tags.mlflow.runName = 'child'")
check('search by run name', len(found2) == 1, len(found2))
mname = 'check-model-' + tag
mv = client.get_model_version(mname, '1')
check('model version registered', mv.run_id == rid, mv)
client.set_registered_model_alias(mname, 'champion', '1')
check('alias', client.get_model_version_by_alias(mname, 'champion').version == '1')
client.update_model_version(mname, '1', description='first fit')
client.set_model_version_tag(mname, '1', 'checked', 'yes')
v = client.get_model_version(mname, '1')
check('version description and tag', v.description == 'first fit' and v.tags.get('checked') == 'yes', v)
loaded = mlflow.pyfunc.load_model('models:/' + mname + '@champion')
pred = loaded.predict(np.array([[5.0]]))
check('model loads by alias and predicts', abs(float(pred[0]) - model.predict(np.array([[5.0]]))[0]) < 1e-9, pred)
check('search model versions', len(client.search_model_versions("name='" + mname + "'")) == 1)
check('registered model listed', any(m.name == mname for m in client.search_registered_models()))
lm = mlflow.search_logged_models(experiment_ids=[exp.experiment_id], output_format='list')
check('logged model', len(lm) == 1 and lm[0].name == 'model', lm)
@mlflow.trace
def add(a, b):
    return a + b
add(2, 3)
try:
    mlflow.flush_trace_async_logging()
except Exception:
    pass
time.sleep(1)
traces = mlflow.search_traces(locations=[exp.experiment_id], return_type='list')
check('a trace kept', len(traces) >= 1, traces)
if traces:
    t = mlflow.get_trace(traces[0].info.trace_id)
    check('trace spans', t is not None and len(t.data.spans) == 1 and t.data.spans[0].name == 'add', t)
p = mlflow.genai.register_prompt(name='greet-' + tag, template='Hello {{name}}!', commit_message='first')
check('prompt registered', p.version == 1)
lp = mlflow.genai.load_prompt('prompts:/greet-' + tag + '/1')
check('prompt loads and formats', lp.format(name='Ada') == 'Hello Ada!', lp)
client.delete_run(child_id)
check('run deleted', client.get_run(child_id).info.lifecycle_stage == 'deleted')
client.restore_run(child_id)
check('run restored', client.get_run(child_id).info.lifecycle_stage == 'active')
check('experiments searched', any(e.name == exp_name for e in client.search_experiments()))
bad = sum(1 for _, ok in results if not ok)
print('%d checks, %d failed' % (len(results), bad))
sys.exit(1 if bad else 0)
