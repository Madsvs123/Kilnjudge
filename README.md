# Kilnjudge

Kilnjudge is a local practice judge for one person. The owner writes or selects algorithm exercises, then runs their own Python solutions against sample tests and hidden tests that stay on the machine.

It is a practice tool for the owner's own algorithm code.

## Who it is for

One operator: the person who owns this checkout. Register an account in the local app, sign in, and submit solutions. Submission history is stored for that signed-in account only.

## Stack

- Backend: Django 5, Django REST Framework, SimpleJWT, SQLite
- Frontend: React 18, TypeScript, Vite, react-router-dom, TanStack Query, axios, zustand, lucide-react, react-hook-form, zod, and clsx

Judging runs the submitted source in a child Python process. Each test has a wall-clock timeout. The child is started with network sockets disabled. Run only your own solutions.

## How to run

From the `backend` directory, using `py -3`:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

`migrate` loads the original exercises (strings, arrays, and digit math), each with a difficulty, topic tags, hints, an editorial note, and its own wall-clock limit. To load them again:

```powershell
.venv\Scripts\python.exe manage.py seed_problems
```

Bundled JSON fixtures, including the extra owner-shelf tag, load with:

```powershell
.venv\Scripts\python.exe manage.py load_fixtures
```

Optional admin account:

```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

From the `frontend` directory:

```powershell
npm install
npm run dev
```

Open http://127.0.0.1:5173 , register, and sign in. The API listens on http://127.0.0.1:8000 . Set `VITE_API_URL` if the API is elsewhere.

The problem list can be filtered by tag. Each statement shows hints that do not give the answer, plus editorial notes the signed-in owner can revise. Check samples before an official submit; a sample check is not stored. History can compare two of your own runs and shows the captured runtime in milliseconds.

Submit a file from the repository root once the API is running:

```powershell
py -3 scripts\kiln_submit.py shelf-gaps solution.py --username kiln-owner --password "local-pass-123"
```

Add `--samples-only` to check samples without storing a submission. Creating a problem is `POST /api/problems/` while signed in. The body includes the statement, tags, a time limit in milliseconds, at least one sample, and at least one hidden test. Hidden tests stay off the response.

On macOS or Linux, create the virtual environment with `python3 -m venv .venv` and call `./.venv/bin/python` instead of the Windows path above.

## Tests and build

Backend, from the `backend` directory:

```powershell
.venv\Scripts\python.exe manage.py test
```

Frontend production build, from the `frontend` directory:

```powershell
npx vite build
```

## License

MIT License. Copyright (c) 2026 Madsvs123.
