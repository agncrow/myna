# Not Built

Everything is built in Crow, with no integration with an outside
framework. These parts of MLflow are left out for that reason:

| MLflow feature | Why not | What Myna has |
|---|---|---|
| Python flavors (scikit-learn, PyTorch, TensorFlow, XGBoost, transformers, …) and serving them | Each is a Python framework | The `crow` flavor; MLflow's client can still store any model's files as artifacts |
| Autologging | It patches Python libraries | Explicit `log_*` calls |
| Cloud artifact stores (S3, Azure, GCS, HDFS) | Outside services | The workspace folder |
| SQL tracking backends | Magpie is the store | Magpie logs |
| Databricks, Unity Catalog, the permissions plugin | Outside platform | Myna's workspace |
| AI Gateway, deployments to SageMaker, Azure ML, Ray | Outside services | Myna's own serving |
| Docker images, conda and virtualenv environments | Python packaging | A model folder run by crow |
| GenAI judges (`mlflow.genai` scorers) | They call outside models | Evaluation's scores, and feedback on traces |
| OpenTelemetry trace export and import (`/v1/traces`, protobuf) | Outside protocol | Traces kept in Myna, spans as JSON |
| Signature inference from Python types | Python | The columns written in `MLmodel` |
| Recipes | Retired in MLflow | Notebooks and jobs |

And these are not built yet, though they are Crow work:

- **The artifact proxy** (`/api/2.0/mlflow-artifacts/…` upload and
  download). MLflow's client writes and reads the workspace's files
  directly, which works when it runs on the same machine. A client
  elsewhere needs the proxy.
- **Projects** (`MLproject` entry points run as jobs).
- **Classifier extras:** log loss, the confusion matrix, and a table of
  every scored row (`eval_results`).
- **On the pages:**
  - previews of images and tables among the artifacts;
  - a value shown on hover over a chart;
  - a diff between two prompt versions;
  - downloading a file.
- **Serving speed.** A served model is started for each request rather
  than kept warm: about a second for each call.
- **A logged-model record for a saved model.** `serving.save_model`
  writes the model's files among the run's artifacts, and a run's page
  lists them under Artifacts. It makes no logged-model record, as MLflow
  3's `log_model` does, so the run's Logged models card stays empty.
  MLflow's client's own `log_model` does make one.

Interpreted (`crow run -i main.co`), the Experiments pages answer a click
in 9 to 17 seconds once a few sessions are open. Each refresh derives
every open page again from the logs. Compiled (`crow run main.co`, the
default), the same click answers in under 0.1 seconds.
