# Tests

```text
./test.sh
```

runs every part's test blocks, interpreted and then compiled, then the
checks against Python ([How Experiments and Models Are
Tested](ml-tests.md)). `./test.sh path/to/crow` tests another crow.

The tests make and remove a workspace of their own, `test_data/`, and
refuse to run in `myna_data/`: an early version of them, run while a
server was up, had removed the workspace it was serving.
