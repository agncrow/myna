# Licensing

Myna is source-available under the [Business Source License 1.1](LICENSE)
(BSL), with an additional use grant. This page says what that means in
plain words; where the two differ, the license decides.

## Free, for everyone

- Reading, changing and sharing the code.
- Development, testing, evaluation, continuous integration, staging and
  demos, on any number of machines.
- **Non-commercial use in production, without limit**: an individual's
  study, research and hobby projects, and charities, schools, public
  research and government.
- **Commercial use in production on one machine per application**: the
  workspace an application's Myna writes and reads is stored on, and
  opened from, one machine.

## Needs a commercial license

- A company's production use of one application on **more than one
  machine**: a workspace on shared or network storage opened by Myna on
  several machines, or one application's workspace split across
  machines.
- Offering Myna, or a product whose main value is Myna, to others as a
  **hosted or managed service**.

## Counting machines

A machine is one physical computer or one virtual machine, with every
process and container on it.

| A second machine (needs a license) | Not a second machine (free) |
|---|---|
| Myna on another machine opening the same workspace | The browsers that open Myna's pages |
| One application's workspace split across machines | MLflow's client, or any program, reaching Myna over HTTP |
| A workspace on network storage, opened from several machines | Backups of the workspace at rest |
| | Restoring onto a replacement machine after a failure |
| | The scheduler, the notebooks' runs and served models: processes on the one machine |

## Forks

A modified copy stays under the same license, whoever modified it and
whatever was added: it may not be used in production beyond these terms,
nor offered as a hosted service, and it may not use the name Myna.

## Four years on

Each version of Myna becomes available under the Apache License 2.0 four
years after it is published: the BSL's change date.

## Contributions

Outside contributions are not accepted yet: a contributor license
agreement will come first.

## Commercial licenses

Write to vkotinaga@gmail.com.
