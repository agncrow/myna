# The Code

Myna is a Crow program of parts, laid out as Magpie's repository is.

| File | What it does |
|---|---|
| `main.co` | Serves the pages |
| `myna/workspace.co` | Reads and writes the logs |
| `myna/tally.co` | A table's size and its columns, read off its files and never off its rows |
| `myna/engine.co` | Makes a notebook into one program, runs it, and reads its output back cell by cell |
| `myna/workbench.co` | The frame every page shares: the sidebar, the top bar and the search |
| `myna/queries.co` | Runs a query, writes it as a cell's Crow, and says it in a line; the dashboards read saved queries through it |
| `myna/tiles.co` | Refreshes a dashboard's tiles and says when one is due |
| `myna/tracking.co` | The experiments' store: runs, params, metrics, tags, datasets, files |
| `myna/registry.co` | Registered models, versions, aliases, stages and prompts |
| `myna/search.co` | MLflow's search grammar, parsed |
| `myna/traces.co` | Traces, spans and feedback |
| `myna/serving.co` | A model's folder, serving and evaluation |
| `myna/mlapi.co` | MLflow's HTTP API over the store, the registry, the search and the traces |
| `myna/charts.co` | The experiments' charts, as SVG |
| `myna/notebooks.co`, `query.co`, `catalog.co`, `dashboards.co`, `jobs.co`, `settings.co` | The workbench's pages |
| `myna/experiments.co`, `runs.co`, `models.co` | The experiments' and models' pages |
| `myna/soon.co` | The page not built yet |
| `scheduler.co` | The scheduler |

Nothing in Myna changes Crow's compiler. A bug Myna met in Crow was fixed
in Crow, with its test, before Myna went on: 31 of them so far, in
three of Crow's commits (f448e81, ce4683d and 8a96a3a).
