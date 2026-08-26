# NBA Model Dashboard Engineering Rules
1. Model/data correctness has priority over visual design.
2. Do not silently change NBA metric semantics.
3. New source integrations require automated tests.
4. Never replace missing model inputs with zero unless conceptually correct.
5. Preserve raw source data where practical.
6. Normalize in processing modules, not JavaScript.
7. Frontend displays data; Python owns data/model logic.
8. Never expose credentials to frontend code.
9. Failed refreshes must preserve the last valid dataset.
10. Maintain desktop, laptop, and iPhone responsiveness.
11. Preserve HTML5 UP attribution while used.
12. Model calculations belong in tested backend code.
13. Run relevant tests before completion.
