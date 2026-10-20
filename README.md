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

`migrate` loads four original exercises (strings, arrays, and digit math). To load them again:

```powershell
.venv\Scripts\python.exe manage.py seed_problems
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
