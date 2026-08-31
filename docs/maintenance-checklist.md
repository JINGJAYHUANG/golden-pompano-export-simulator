# Maintenance checklist

Before each software release:

- [ ] scenario schema and package version are consistent;
- [ ] mass and price definitions have not changed silently;
- [ ] all 523 tests are present and pass;
- [ ] both synthetic Golden fixtures regenerate;
- [ ] nine tamper attacks are detected;
- [ ] public and documentation audits pass;
- [ ] Wheel builds are byte-identical under the fixed epoch;
- [ ] clean-environment installation succeeds;
- [ ] changelog, model card, data card and release claim are current;
- [ ] no real commercial or personal data is present;
- [ ] the release tag is immutable and matches the built source.
