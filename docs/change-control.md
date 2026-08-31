# Model change control

Any change capable of altering seller profit, buyer landed cost, mass balance, quote targets or responsibility allocation must include:

1. a written problem statement;
2. the old and new calculation contract;
3. at least one positive test;
4. at least one negative or boundary test;
5. regenerated synthetic Golden fixtures;
6. a statement of affected unit bases and outputs;
7. a migration or explicit schema-version decision;
8. public-boundary review;
9. an independent review note describing what remains unverified.

Changes must not be justified only by producing a more attractive margin. Negative outputs and newly discovered costs are valid model improvements.
