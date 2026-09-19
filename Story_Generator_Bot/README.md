# Story Generator Bot

Domain: Fiction & Story Development

Local-first Flask + Gemini chatbot. No login/register, Firebase or SQL.

## Windows
```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
Edit `.env` and add your own Gemini API key, then:
```powershell
.\venv\Scripts\python.exe app.py
```
Open http://127.0.0.1:5000

If PowerShell activation is blocked, do not activate the venv; use the direct Python command above.

## Later deployment
Build: `pip install -r requirements.txt`
Start: `gunicorn app:app`
Set `PORT` in the environment if needed.

## Future updates
Change title, domain, system prompt, welcome message, colors, tools, model and port in `config.py`. Add backend routes in `app.py` and UI in `templates/index.html`.

Chat history is temporary and session-based. No global conversation store is used.
