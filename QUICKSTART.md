# 🚀 Quick Start Guide

## Your College Assistant Chatbot is Ready! 

All project files have been created. Follow these simple steps to get it running:

---

## Step 1️⃣: Add Your OpenAI API Key

**File:** `.env`

Open the `.env` file and replace:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

With your real API key from https://platform.openai.com/api-keys

> ⚠️ **Important:** Never share this key! Keep it secret and safe.

---

## Step 2️⃣: Install Python Packages

Open **PowerShell** and run:

```powershell
cd "C:\Users\user\OneDrive\Desktop\college assitant chatbot"
pip install -r requirements.txt
```

**This installs:**
- ✓ Flask (web framework)
- ✓ OpenAI SDK (Python library for GPT)
- ✓ python-dotenv (loads API key from .env)

Wait for all packages to install. You should see a ✓ next to each one.

---

## Step 3️⃣: Run the Chatbot

Still in PowerShell:

```powershell
python app.py
```

You should see:
```
==================================================
College Assistant Chatbot Starting...
==================================================
✓ Database initialized
✓ College data loaded
✓ OpenAI client configured

🌐 Server running at: http://127.0.0.1:5000
📖 Open this URL in your browser to use the chatbot

Press CTRL+C to stop the server
==================================================
```

---

## Step 4️⃣: Open in Browser

**Copy and paste this URL** in your browser:
```
http://127.0.0.1:5000
```

You should see the **College Assistant Chatbot** interface!

---

## Step 5️⃣: Test It!

Try asking questions like:

- "What are the admission requirements?"
- "What courses does Computer Science offer?"
- "What are the library timings?"
- "Tell me about placement"
- "How much are the fees?"

---

## 📁 Project Files Created

```
college assitant chatbot/
├── app.py                    # Flask backend ⭐ Main Python file
├── requirements.txt          # Python packages
├── .env                      # Your API key goes here
├── README.md                 # Project overview
├── SETUP_GUIDE.md           # Detailed guide
├── QUICKSTART.md            # This file
│
├── data/
│   ├── college_data.json    # Sample college info
│   └── chat_db.py           # Database functions
│
├── templates/
│   └── index.html           # Chatbot UI
│
└── static/
    ├── style.css            # Styling
    └── script.js            # Frontend logic
```

---

## ⚙️ How It Works (In Simple Terms)

1. You type a question in the browser
2. JavaScript sends it to Flask backend
3. Flask sends it to OpenAI API
4. OpenAI returns an answer
5. Flask sends it back to browser
6. You see the answer in the chat

```
Browser → Flask → OpenAI → Flask → Browser
```

---

## 🎓 Understanding the Code

### `app.py` (Backend - Python)
- Handles HTTP requests
- Calls OpenAI API
- Saves chat history to database
- Returns responses

### `templates/index.html` (Frontend - HTML)
- The chat interface
- Input box and send button
- Message display area

### `static/script.js` (Frontend - JavaScript)
- Sends questions to backend
- Displays messages
- Handles user interactions

### `static/style.css` (Frontend - CSS)
- Makes it look pretty
- Purple gradient, rounded buttons
- Responsive for mobile

### `data/college_data.json`
- Contains college info
- Used as context for AI
- Edit this to change college information

---

## ✅ Checklist

- [ ] API key added to `.env`
- [ ] Packages installed with `pip install -r requirements.txt`
- [ ] Server running with `python app.py`
- [ ] Browser opened to `http://127.0.0.1:5000`
- [ ] Asked a test question
- [ ] Got an AI response

---

## 🐛 Common Issues

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### "API key not configured"
Check `.env` file has valid `OPENAI_API_KEY`

### "Port 5000 already in use"
Edit `app.py` line 127 to use different port (5001, 5002, etc.)

### "Cannot connect to browser"
- Make sure Flask is running (see terminal)
- URL must be exactly: `http://127.0.0.1:5000`
- Try a different browser if one doesn't work

---

## 📚 Documentation Files

- **README.md** - Full project overview
- **SETUP_GUIDE.md** - Detailed setup and learning guide
- **Code Comments** - Read the comments in Python/JS files

---

## 🎯 Next Steps After Testing

1. **Modify college data** - Edit `data/college_data.json`
2. **Customize UI** - Change colors/fonts in `static/style.css`
3. **Learn the code** - Read comments in `app.py` and `script.js`
4. **Add features** - Database history, file uploads, etc.

---

## 🎉 You're All Set!

Your chatbot is ready to use. Have fun and happy learning! 🚀

**Questions?** Check the code comments - everything is explained!

---

**Still need help?** Read:
- SETUP_GUIDE.md for detailed instructions
- README.md for project overview
