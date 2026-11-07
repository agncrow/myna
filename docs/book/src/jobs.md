# Jobs and the Scheduler

The Jobs page (`/jobs`) shows the scheduler, the schedules and every
run.

## The scheduler

A notebook's schedule is kept in the workspace (`_schedules`), and the
scheduler runs it. The Jobs page starts the scheduler as a process of
its own:

```text
crow run -i scheduler.co 3800
```

Every fifteen seconds it runs the notebooks that are due, and records
each run as the schedule's. It also refreshes the dashboards that are
due. It ends when the page asks it to, or when the page has not answered
for three rounds.

`crow run scheduler.co` runs it without a page, until the file
`myna_data/_scheduler.stop` is written.
