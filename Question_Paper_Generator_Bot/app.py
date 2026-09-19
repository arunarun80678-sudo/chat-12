from flask import Flask,render_template,request,jsonify,session
from dotenv import load_dotenv
from config import BOT_CONFIG
import os
load_dotenv()
app=Flask(__name__)
app.secret_key=os.getenv("FLASK_SECRET_KEY") or BOT_CONFIG["secret_key"]
app.config.update(SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE="Lax",SESSION_COOKIE_SECURE=False)
KEY=os.getenv("GEMINI_API_KEY","").strip(); MODEL=os.getenv("GEMINI_TEXT_MODEL",BOT_CONFIG["gemini_model"])
client=None
if KEY:
    try:
        from google import genai
        client=genai.Client(api_key=KEY)
    except Exception: client=None
def fallback(): return BOT_CONFIG["offline_message"]
def ask(msg):
    if not client:return fallback()
    hist=session.get("chat_history",[])[-BOT_CONFIG["max_history"]:]
    convo="\n".join(x["role"].upper()+": "+x["content"] for x in hist)
    prompt=BOT_CONFIG["system_prompt"]+"\n\nConversation:\n"+convo+"\nUSER: "+msg+"\nASSISTANT:"
    try:
        r=client.models.generate_content(model=MODEL,contents=prompt)
        return (getattr(r,"text","") or fallback()).strip()
    except Exception:return fallback()
@app.get("/")
def home():return render_template("index.html",bot=BOT_CONFIG)
@app.get("/api/health")
def health():return jsonify(status="ok",bot=BOT_CONFIG["title"],gemini_configured=bool(client),model=MODEL)
@app.get("/api/history")
def history():return jsonify(history=session.get("chat_history",[]))
@app.post("/api/chat")
def chat():
    d=request.get_json(silent=True) or {}; msg=(d.get("message") or "").strip()
    if not msg:return jsonify(error="Please enter a message."),400
    reply=ask(msg); h=session.get("chat_history",[])
    h += [{"role":"user","content":msg},{"role":"assistant","content":reply}]
    session["chat_history"]=h[-BOT_CONFIG["max_history"]:]; session.modified=True
    return jsonify(reply=reply)
@app.post("/api/clear")
def clear():session.pop("chat_history",None);session.modified=True;return jsonify(ok=True)
if __name__=="__main__":
    app.run(host="127.0.0.1",port=int(os.getenv("PORT",BOT_CONFIG["port"])),debug=False)
