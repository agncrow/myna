# MLflow's Known Bugs, and How Myna Avoids Them

MLflow's issue tracker was read for bugs in the parts Myna rebuilds, and
the ones that apply are held off by design:

- **Zero is a value.** A step or a time of 0 is kept, not read as
  missing.
- **NaN.** NaN is stored and shown as NaN. It fails every comparison and
  sorts last.
- **History.** The history of a key never logged is an empty list, in
  step-then-time order.
- **The latest metric** is the one at the greatest step, not the last
  row written.
- **Search is parsed, never pasted into a query.**
  - Numbers compare as numbers.
  - Operators may be in any case, either quote mark may be used, and
    backticked keys are read.
  - Paging has one stable order with the id last, so no run is seen
    twice or skipped.
  - A bad page token or `IS NULL` is refused with
    `INVALID_PARAMETER_VALUE`.
- **Names.** An experiment's name, deleted or not, stays taken. Default
  (id 0) is made once.
- **Renames.**
  - A run's rename changes its name and its `mlflow.runName` tag only.
  - A registered model's rename moves its tags, aliases and versions.
- **Deleted versions.** Deleting a version removes its aliases.
- **Stages.** `archive_existing_versions` archives every other version
  in the stage.
- **Files.**
  - A path with `..`, an absolute path or a backslash is refused.
  - A version's source must lie among its run's files.
  - A missing file answers with the relative path, never the server's.
- **Prompts.** A prompt is formatted in one pass, so a value's text is
  never formatted again.
- **Charts** are sorted by x with y fitted to the data, and children
  stay under their parent at any sort.
