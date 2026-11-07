# Installing and Running Myna

Myna needs Crow 0.8.2 or later: building Myna found 31 bugs in Crow,
and 0.8.2 is the release that fixes them. Crow installs in one line,
fetching a C toolchain and Rust if they are missing:

```text
curl -fsSL https://raw.githubusercontent.com/agncrow/crow/main/install.sh | bash
```

[the Crow Book](https://agncrow.github.io/crow/) says more. Then get
Myna, install Magpie (its one dependency, pinned by `crow.lock`) and
start it:

```text
git clone https://github.com/agncrow/myna
cd myna
crow install
crow run main.co
```

`crow run main.co` builds the compiled program and serves it on
<http://localhost:3800>. The first build takes a few minutes; an edit
rebuilds in seconds.

`crow run -i main.co` interprets it instead, with no build. It still
reads the whole program before it serves: from a fresh clone that took
138 seconds on the Mac Studio it was timed on. Every
page works the same way in both modes, but the interpreter derives each
open page again from the logs on every refresh. Once a few sessions are
open, a click on an Experiments page took 9 to 17 seconds interpreted,
against under 0.1 seconds compiled. These are times seen while checking
the pages in a browser, not a benchmark. Use the compiled program for
real work, and the interpreter for a quick look.

## The workspace folder

Myna keeps everything in `myna_data/` beside the program. `MYNA_DATA`
names another folder:

```text
MYNA_DATA=my_workspace crow run main.co
```

The folder must lie inside Myna's checkout, where the programs a
notebook runs find `crow_modules/`.

## Sample data

`tests/mlflow/house_prices.co` trains, registers, evaluates and serves a
small model, so the Experiments and Models pages have something to show:

```text
crow run -i tests/mlflow/house_prices.co
```

It adds an experiment and a model to the workspace and deletes nothing.
Put `MYNA_DATA=…` in front of both commands to keep the sample out of
your own workspace.
