# College Assistant Chatbot - Setup & Run Guide

## 📁 Project Structure

Your project now has this structure:

```
college assitant chatbot/
├── app.py                          # Main Flask backend (Python)
├── requirements.txt                # Python packages to install
├── .env                            # Environment variables (API key)
│
├── data/
│   ├── college_data.json          # Sample college information
│   └── chat_db.py                 # Database module for chat history
│
├── templates/
│   └── index.html                 # Chatbot UI (HTML)
│
└── static/
    ├── style.css                   # Styling (CSS)
    └── script.js                   # Frontend logic (JavaScript)
```

---

## 🔑 Step 1: Add Your OpenAI API Key

1. **Open `.env` file** in your project
2. **Replace the placeholder** with your actual API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
FLASK_ENV=development
FLASK_DEBUG=True
```

**Where to get your API key:**
- Go to https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy the key and paste it in `.env`
- Keep this key SECRET - never share it

---

## 📦 Step 2: Install Python Packages

Open PowerShell and run:

```powershell
# Navigate to your project folder
cd "C:\Users\user\OneDrive\Desktop\college assitant chatbot"

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `Flask==2.3.3` - Web framework for building the server
- `python-dotenv==1.0.0` - Loads API key from .env file
- `openai==1.3.0` - OpenAI Python SDK to interact with GPT models

Wait for the installation to complete. You should see ✓ marks next to each package.

---

## 🚀 Step 3: Run the Chatbot

In PowerShell, run:

```powershell
# Make sure you're in the correct folder
cd "C:\Users\user\OneDrive\Desktop\college assitant chatbot"

# Start the Flask server
python app.py
```

You should see output like:

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

## 🌐 Step 4: Open the Chatbot in Browser

1. **Copy this URL**: `http://127.0.0.1:5000`
2. **Paste it in your browser** (Chrome, Firefox, Edge, etc.)
3. **You should see the chatbot UI**

---

## 💬 Step 5: Test the Chatbot

Try asking these questions to test:

1. **"What are the admission requirements?"**
   - The chatbot will answer based on college data

2. **"What courses does the Computer Science department offer?"**
   - It will find and list the courses

3. **"What are the library timings?"**
   - It will show library opening/closing times

4. **"Tell me about placement"**
   - It will share placement statistics

5. **"How much are fees?"**
   - It will provide fee information

---

## 📝 Understanding the Code

### app.py (Flask Backend)

**What it does:**
1. Loads your `.env` file to get the API key
2. Creates a Flask web server
3. Loads college data from `college_data.json`
4. Receives questions from the frontend (HTML)
5. Sends them to OpenAI using the Python SDK
6. Returns AI response to frontend
7. Saves conversations to SQLite database

**Key functions:**
- `create_system_prompt()` - Creates the instruction prompt for AI
- `@app.route("/")` - Serves the HTML chatbot UI
- `@app.route("/api/chat", methods=["POST"])` - Receives questions and returns answers
- `@app.route("/api/history")` - Retrieves chat history

### data/college_data.json

**Contains:**
- College name, location, contact info
- Departments and courses
- Admission information
- Fees
- Library timings
- Placement data
- Attendance rules
- Campus facilities

**How it's used:**
- Loaded into memory when server starts
- Included in the system prompt sent to OpenAI
- Used as context for all AI responses

### data/chat_db.py

**Database functions:**
- `init_database()` - Creates SQLite table
- `save_chat(name, question, answer)` - Stores Q&A in database
- `get_chat_history(name, limit=10)` - Retrieves past conversations

### templates/index.html

**The Chatbot UI includes:**
- Header with college name
- Message display area
- Student name input
- Question input field
- Send button
- Character counter
- Footer with tips

### static/style.css

**Styling features:**
- Purple gradient background
- Rounded message bubbles
- Different colors for student (blue) and bot (gray) messages
- Responsive design for mobile
- Smooth animations and transitions

### static/script.js

**Frontend logic:**
- Sends questions to backend via `/api/chat`
- Displays messages in chat
- Manages conversation history
- Handles errors gracefully
- Updates character count
- Formats messages with line breaks and bold/italic

---

## ⚙️ How the Chatbot Works (Step by Step)

```
1. USER TYPES QUESTION
        ↓
2. JavaScript gets text from input box
        ↓
3. Displays question in chat as blue bubble
        ↓
4. Sends to backend: POST /api/chat
        ↓
5. Flask receives question
        ↓
6. Creates system prompt with college data
        ↓
7. Calls OpenAI API with:
   - System prompt (instructions)
   - Previous messages (context)
   - Current question
        ↓
8. OpenAI returns AI response
        ↓
9. Flask saves Q&A to database
        ↓
10. Returns response to frontend
        ↓
11. JavaScript displays as gray bubble
        ↓
12. User reads response
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install -r requirements.txt` again

### "API key not configured"
**Solution:** Make sure your .env file has a valid `OPENAI_API_KEY`

### "Port 5000 already in use"
**Solution:** Either:
- Close other Flask apps using port 5000
- Or change port in `app.py` line 127: `app.run(debug=True, host="127.0.0.1", port=5001)`

### "Cannot find college_data.json"
**Solution:** Make sure you're running from the correct folder with `cd`

### API request timeout
**Solution:** Check your internet connection and API key validity

### "college_data.json not found" error
**Solution:** Make sure file exists at `data/college_data.json`

---

## 🎓 Key Learning Points

### Python Concepts Used:
- **Functions** - Reusable blocks of code
- **Dictionaries** - Storing data like college info
- **Lists** - Chat history array
- **Strings** - Text manipulation
- **JSON** - Data format for college info
- **Exception Handling** - try/except for errors

### Flask Concepts:
- **Routes** - URL endpoints (@app.route)
- **POST/GET** - HTTP methods
- **JSON** - Request/response format
- **Templates** - HTML with Jinja2 syntax

### JavaScript Concepts:
- **Async/Await** - Handling API calls
- **Fetch API** - Making HTTP requests
- **DOM Manipulation** - Changing HTML
- **Event Listeners** - User interactions

### Frontend Concepts:
- **HTML** - Structure (UI layout)
- **CSS** - Styling (colors, fonts, layout)
- **JavaScript** - Interactivity (buttons, messages)

---

## 🚀 Next Steps (Future Enhancements)

1. **Add more college data** - Expand college_data.json
2. **User authentication** - Login system
3. **Chat history persistence** - Load previous conversations
4. **Multi-language support** - Answer in different languages
5. **File upload** - Upload documents for Q&A
6. **Feedback system** - Rate chatbot responses
7. **Admin panel** - Manage college data without coding
8. **Mobile app** - Native iOS/Android version

---

## 📞 Support

If you face issues:
1. Check error message in terminal
2. Read the comment in the problematic code section
3. Check the Troubleshooting section above
4. Review the code comments in app.py, script.js

---

## ✅ Complete!

Your College Assistant Chatbot is now ready to use! 🎉

**Quick recap:**
- ✓ Python backend (Flask + OpenAI SDK)
- ✓ Interactive frontend (HTML/CSS/JavaScript)
- ✓ College data management (JSON)
- ✓ Chat history (SQLite database)
- ✓ Error handling and validation
- ✓ Responsive design for mobile

Happy learning! 🚀
