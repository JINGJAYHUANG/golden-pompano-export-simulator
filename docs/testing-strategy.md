# Testing strategy

The test suite uses four forms of evidence.

## Example-based tests

Named cases verify mass balance, seller/buyer bridges, quote targets, CLI behavior, SQLite output and explicit public boundaries.

## Matrix tests

Systematic combinations cover:

- 120 glaze/target-mass combinations;
- 120 cost-basis/rate combinations;
- 100 invalid-input boundary cases;
- 100 break-even and target-margin solver cases;
- 40 hash-chain integrity cases.

Together with 43 core tests, the release inventory is exactly 523 tests.

## Golden fixtures

Two fictional scenarios are committed with deterministic output bundles. CI regenerates each bundle and compares all ordinary files byte-for-byte. SQLite is compared by ordered table content and schema.

## Red-team integrity tests

Nine attacks alter inputs, calculations, reports, SQLite, event order, artifact presence or manifest identity. Every attack must be detected before release.

The suite validates implementation behavior under declared assumptions. It does not validate any live price, contract, tax rule or commercial outcome.
