# Further judge work

Kilnjudge stays a local practice judge for one person. The owner writes original exercises and runs their own Python against them. Judging keeps the child process without network sockets and with the wall-clock limit stored on that problem.

## Catalog

- Add more original exercises in the same voice as the current set. Each one needs samples, hidden tests, a difficulty, tags, and a time limit.
- Keep hints as nudges. A hint may name the shape of the walk through the input. It should not state the answer or paste a solution.
- Keep editorial notes as the owner's own write-up, edited from the problem page after the exercise makes sense.
- Let the owner retire a problem from the practice list without deleting its submission history.

## Judging

- Report the first failing sample by number, and keep hidden inputs on the server.
- Keep the sample check separate from an official submit so a draft run is not stored.
- Store the milliseconds already captured, and add a per-test breakdown beside the total.
- Reject a submit that is empty or larger than the current source limit before a process is started.

## Practice desk

- Page the history list once it grows past a single screen.
- Let the owner export their own submissions as JSON, including verdict, milliseconds, and source.
- Remember the last tag filter in the browser so a return visit opens on the same topic.
- Offer the starter snippet from the statement's input shape, still without a solution filled in.

## Care

- Keep the MIT license on the repository.
- Keep the virtual environment, frontend dependencies, the production build, and the SQLite database out of git.
- Run the Django tests and the frontend production build before publishing a change that touches judging or the practice pages.
