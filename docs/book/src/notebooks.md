# Notebooks

The Notebooks page (`/`) lists the workspace's notebooks. A notebook is
a list of cells of Crow.

## Running a notebook

A run takes the cells top to bottom as **one program**, run by the crow
on the PATH in the workspace's folder. So a name one cell sets is there
in the next, and a table a cell writes is a Magpie log beside the
others, which the Catalog then shows.

Under each cell are its output, its status and how long it took:

- A stop or a refusal is shown under the cell it names, by the cell's
  own line, and the cells after it are skipped.
- A run that takes longer than the workspace allows (60 seconds unless
  Settings says otherwise) is stopped.
- The side panel names the variables the cells left and the tables they
  read and write.

## Keys

| Key | Does |
|---|---|
| Ctrl+Enter | Run |
| Ctrl+S | Save |
| Escape | Cancel an edit |

## History

Every save is a version, and every run is kept with its output. History
lists both: it opens a run's output, and restores a version.

## A schedule

A notebook can run on a schedule, which the scheduler keeps (see
[Jobs and the Scheduler](jobs.md)). Each scheduled run is recorded
as the schedule's, and the Jobs page lists it.

## Logging experiments

A cell that trains a model logs into Experiments with a few calls: see
[Logging from a Notebook](logging.md).
