# Dashboards

A dashboard (`/dashboards`) sets saved queries side by side as tiles.
Each tile is drawn as bars, a number or a table.

- A query is added from the dashboard, or pinned from the Query page.
- Tiles are moved and removed in place.
- **Refresh now** asks every tile's query again.
- A dashboard given an interval (1 min, 15 min, 1 h or 1 d) is
  refreshed by the scheduler.

Each tile's answer is kept as a Parquet file under `.tiles/`, so a
dashboard opens without asking its queries again. The dashboards are
kept in the `_dashboards` log, their tiles in `_tiles`.
