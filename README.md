<p align="center"><img src="assets/myna.svg" width="128" alt="Myna"></p>

# Myna

A workbench over [Magpie](https://github.com/agncrow/magpie), written in
Crow: the catalog, queries, notebooks, dashboards, models, a model to ask
and the jobs that run it all, every piece of its state a Magpie log. The
first page is the notebook.

Myna needs Crow 0.8.0 or later and installs Magpie as any dependency:

```
crow install
crow run main.co
```

serves it on port 3800. A notebook is cells of Crow, run top to bottom as
one program by the crow on the PATH, each cell's output shown under it;
every save is a batch in `myna_data/notebooks`, so a notebook's history
is its log, and `latest` is the notebook.

```
crow test main.co
```

runs its blocks: a notebook made, written, run and read back from the
log, and a refusal shown under the cell that caused it.

The design, the screens and the plan: the architecture document and the
design canvas (private for now). The name: the myna, the clever talking
bird of every Indian town; the mark is Crow's face between two amber
quotation marks, `"(o.o)"`, the one that talks.

## License

Business Source License 1.1: `LICENSE`, in plain words in `LICENSING.md`.
Free for development, testing and non-commercial use, and for commercial
production on one machine per application; hosted services need a
commercial license (vkotinaga@gmail.com). Each version becomes
Apache-2.0 four years after it is published.
