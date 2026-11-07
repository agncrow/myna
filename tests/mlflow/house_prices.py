"""The house-prices run held to Python: the same 200 houses made the same
way, the same gradient descent in plain Python loops (the same order of
additions, so the same floats), scikit-learn's scores of the held-out rows
and the served model's predictions — every number Myna's run prints,
compared.

    ~/.venvs/mlflow/bin/python tests/mlflow/house_prices.py [crow] [--compiled]

It runs tests/mlflow/house_prices.co with the crow given (the PATH's by
default), interpreted, or compiled with --compiled, in a scratch MYNA_DATA,
and fails naming the first number that differs.
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile

from sklearn import metrics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def house(i):
    area = 50.0 + float((i * 37) % 150)
    rooms = float(1 + i % 5)
    age = float((i * 13) % 40)
    noise = float((i * 7919) % 2001 - 1000) * 10.0
    return area, rooms, age, 1000.0 * area + 5000.0 * rooms - 300.0 * age + 20000.0 + noise


def centre(xs):
    total = 0.0
    for x in xs:
        total = total + x
    return total / float(len(xs))


def spread(xs, c):
    total = 0.0
    for x in xs:
        total = total + (x - c) * (x - c)
    return math.sqrt(total / float(len(xs)))


def train(lr, epochs, xs0, xs1, xs2, ys):
    n = float(len(ys))
    w0 = w1 = w2 = b = 0.0
    last = 0.0
    curve = []
    for _ in range(epochs):
        g0 = g1 = g2 = gb = squares = 0.0
        for i in range(len(ys)):
            err = b + w0 * xs0[i] + w1 * xs1[i] + w2 * xs2[i] - ys[i]
            squares = squares + err * err
            gb = gb + err
            g0 = g0 + err * xs0[i]
            g1 = g1 + err * xs1[i]
            g2 = g2 + err * xs2[i]
        last = math.sqrt(squares / n)
        curve.append(last)
        b = b - lr * gb / n
        w0 = w0 - lr * g0 / n
        w1 = w1 - lr * g1 / n
        w2 = w2 - lr * g2 / n
    return dict(lr=lr, w=(w0, w1, w2), b=b, rmse=last, curve=curve)


def expected():
    houses = [house(i) for i in range(200)]
    test = [h for i, h in enumerate(houses) if i % 5 == 0]
    train_set = [h for i, h in enumerate(houses) if i % 5 != 0]
    cols = list(zip(*train_set))
    c = [centre(cols[k]) for k in range(3)]
    s = [spread(cols[k], c[k]) for k in range(3)]
    xs = [[(x - c[k]) / s[k] for x in cols[k]] for k in range(3)]
    fits = [train(lr, 60, xs[0], xs[1], xs[2], list(cols[3])) for lr in (0.3, 0.1, 0.03)]
    best = fits[0]
    for f in fits[1:]:
        if f['rmse'] < best['rmse']:
            best = f

    def predict(area, rooms, age):
        # the served program's arithmetic: each feature standardized, then
        # the bias and the three products added left to right
        x0 = (area - c[0]) / s[0]
        x1 = (rooms - c[1]) / s[1]
        x2 = (age - c[2]) / s[2]
        return best['b'] + best['w'][0] * x0 + best['w'][1] * x1 + best['w'][2] * x2

    truth = [h[3] for h in test]
    predicted = [predict(h[0], h[1], h[2]) for h in test]
    scores = {
        'mean_squared_error': metrics.mean_squared_error(truth, predicted),
        'root_mean_squared_error': metrics.root_mean_squared_error(truth, predicted),
        'mean_absolute_error': metrics.mean_absolute_error(truth, predicted),
        'r2_score': metrics.r2_score(truth, predicted),
        'max_error': metrics.max_error(truth, predicted),
        'mean_absolute_percentage_error': metrics.mean_absolute_percentage_error(truth, predicted),
    }
    served = [predict(120.0, 3.0, 10.0), predict(80.0, 2.0, 35.0), predict(199.0, 5.0, 0.0)]
    return c, s, fits, best, scores, served


def run_crow(crow, compiled):
    data = tempfile.mkdtemp(prefix='myna_hp_')
    try:
        env = dict(os.environ, MYNA_DATA=data)
        args = [crow, 'run', 'tests/mlflow/house_prices.co'] if compiled else [crow, 'run', '-i', 'tests/mlflow/house_prices.co']
        r = subprocess.run(args, cwd=ROOT, env=env, capture_output=True, text=True, timeout=1200)
        if r.returncode != 0:
            sys.exit('crow failed:\n' + r.stdout + r.stderr)
        return r.stdout.splitlines()
    finally:
        shutil.rmtree(data, ignore_errors=True)


def near(a, b, rel):
    return a == b or abs(a - b) <= rel * max(abs(a), abs(b))


def main():
    argv = [a for a in sys.argv[1:] if a != '--compiled']
    crow = argv[0] if argv else 'crow'
    compiled = '--compiled' in sys.argv
    c, s, fits, best, scores, served = expected()
    lines = run_crow(crow, compiled)
    failures = []

    def same(what, got, want, rel=0.0):
        if not near(got, want, rel):
            failures.append(f'{what}: crow {got!r}, python {want!r}')

    words = lines[0].split()
    for k in range(3):
        same(f'centre {k}', float(words[1 + k]), c[k])
        same(f'spread {k}', float(words[5 + k]), s[k])
    for f, line in zip(fits, [l for l in lines if l.startswith('lr ')]):
        w = line.split()
        same(f'lr {f["lr"]}', float(w[1]), f['lr'])
        for k in range(3):
            same(f'lr {f["lr"]} w{k}', float(w[3 + k]), f['w'][k])
        same(f'lr {f["lr"]} b', float(w[7]), f['b'])
        same(f'lr {f["lr"]} rmse', float(w[9]), f['rmse'])
    registered = [l for l in lines if l.startswith('registered ')][0].split()
    same('the best run', float(registered[4]), best['lr'])
    got_scores = {l.split()[1]: float(l.split()[2]) for l in lines if l.startswith('score ')}
    if set(got_scores) != set(scores):
        failures.append(f'scores: crow {sorted(got_scores)}, python {sorted(scores)}')
    for key, want in scores.items():
        # scikit-learn sums with numpy (pairwise, vectorized): the last digits
        # of a sum may differ from a loop's, never more
        same(f'score {key}', got_scores.get(key, float('nan')), want, rel=1e-12)
    served_line = [l for l in lines if l.startswith('served ')][0]
    import json
    got_served = json.loads(served_line[len('served '):])['predictions']
    for k, want in enumerate(served):
        same(f'served prediction {k}', got_served[k], want)
    mode = 'compiled' if compiled else 'interpreted'
    if failures:
        sys.exit(f'house prices ({mode}): {len(failures)} differ\n' + '\n'.join(failures))
    print(f'house prices ({mode}): every number agrees with Python — 3 runs × 60 epochs, '
          f'{len(scores)} scores, {len(served)} served predictions')


if __name__ == '__main__':
    main()
