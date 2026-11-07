# Query and the Catalog

## The Catalog

The Catalog (`/catalog`) lists the workspace's tables, each a Magpie
log, with their columns and their latest rows. **Query this table**
opens the Query page on it.

## Query

The Query page (`/query`) asks one of Magpie's reading verbs of a
table, as a form:

- **Latest rows**: the columns named, or all.
- **A summary**: grouped by columns, a column reduced by sum, count,
  mean, min, max, std, var, first or last, over the rows a predicate
  admits.
- **A search** of a text column: words, phrases, prefixes (`kit*`) and
  fuzzy words (`kitchn~`).

The answer is a table and, for a summary, bars.

A query is saved by name in the workspace's `_queries` log and opened
again from the list. **Open as notebook** writes it as the first cell
of a new notebook, so a question asked as a form can grow into a
program. **Pin to** puts it on a dashboard.
