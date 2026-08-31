# Versioning policy

The project uses semantic versions for the software package and an independent `schema_version` for scenario contracts.

- Patch release: calculation bug fix or documentation correction that preserves the `1.0` scenario contract.
- Minor release: additive capability, new output or optional field that preserves existing valid scenarios.
- Major release: incompatible calculation semantics, removed field or changed mass/price definition.

A software release must not silently reinterpret an existing scenario. When a mass, tax, quote or responsibility convention changes, the scenario schema version must change or a migration must make the transformation explicit.

Published Git tags are immutable. A correction after release receives a new version; an existing tag must not be moved to different source.
