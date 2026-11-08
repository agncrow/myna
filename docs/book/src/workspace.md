# The Workspace and Settings

## The workspace

Code is files in a project; data is logs in Magpie. Myna's own folder,
`myna_data/` unless `MYNA_DATA` names another, holds the workspace's
records and the scratch project, the one worked in while no project is
open:

| In Myna's folder | Holds |
|---|---|
| `_users`, `_grants` | who may sign in, and their grants on projects |
| `_projects` | the projects opened (Projects) |
| `scratch/` | the scratch project: a `crowfile`, `myna.json`, `notebooks/`, `queries/`, `data/` |

| In a project | Holds |
|---|---|
| `notebooks/<name>.co` | a notebook: a Crow program, its cells marked by `--- %%` lines |
| `queries/<name>.json` | a saved query |
| `myna.json` | the dashboards and their tiles, the schedules, the settings |
| `data/_runs` | every run and its output |
| `data/_answers`, `data/.tiles/` | each tile's last refresh and its kept answer |
| `data/_ml_*` | experiments and models ([how](mlflow.md)) |
| `data/<any other name>` | a table a program or a notebook wrote |

A log's change is a new row, and a read takes the latest row per key, so
nothing is edited in place and the history of every record is kept. A
file's history is git's.

## Settings

The Settings page (`/settings`) holds the workspace's name, and how long
a run may take before it is stopped (60 seconds unless set). An admin
changes them.

## Users and access

A workspace with no users is one person's own: the reader is the account
Myna runs as, an admin, and no page asks for a sign-in. The Users page
(`/users`) adds the first user — an admin, whatever role was asked — and
signs you in as them; from then on every page asks for a sign-in, and a
page draws nothing else until one is given. A user has a role: an admin
does everything, a member what their grants allow. The Access page
(`/access`) gives a member a grant on a project: a viewer reads it, an
editor reads and writes, an owner grants too. A reader with no grant on
the open project is told so, and a reader without an editor's grant
changes nothing: the handlers that write refuse them. Passwords are kept
as Crow's password hash (Argon2id), never as themselves, and the sign-in
is Crow's signed cookie, good for thirty days or until Sign out. Where
this is going — projects as apps built on Myna, a server many people
share — is `docs/platform.md`.

## Search

The search in the top bar finds notebooks and tables by name.
