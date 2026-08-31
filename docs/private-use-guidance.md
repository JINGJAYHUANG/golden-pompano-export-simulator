# Private-use guidance

Keep real scenarios outside the public checkout when practical:

```text
private-workspace/
├── scenarios/
├── evidence/
├── runs/
└── approvals/
```

Recommended controls:

- restrict access by role;
- encrypt storage and backups;
- avoid embedding credentials in scenarios;
- retain source and validity evidence separately;
- record who approved the final quote;
- publish only a reduced synthetic reproduction when reporting a software problem;
- verify a run before relying on a transferred bundle;
- apply an explicit retention and deletion policy.

The repository `.gitignore` excludes common private-input and run directories, but ignore rules are not an access-control system.
