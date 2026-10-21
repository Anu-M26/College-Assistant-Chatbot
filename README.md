# 🎓 College Assistant Chatbot

A modern, interactive chatbot built with Python and Flask that helps students get instant answers to college-related questions using OpenAI's GPT models.

## 🌟 Features

✅ **AI-Powered Responses** - Uses OpenAI GPT-3.5-turbo to understand and answer questions  
✅ **College Context** - Trained on college information (departments, fees, admission, etc.)  
✅ **Conversation History** - Maintains context across multiple messages  
✅ **Modern UI** - Beautiful, responsive web interface  
✅ **Database Storage** - Saves all conversations for future reference  
✅ **Error Handling** - Graceful error messages and validation  
✅ **Beginner-Friendly** - Well-commented code for learning Python and Flask  

## 🛠️ Tech Stack

- **Backend:** Python, Flask, OpenAI SDK
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **API:** OpenAI ChatGPT API

## 📋 Questions the Chatbot Can Answer

- **Admission Info** - Eligibility, entrance exam, application deadline, fees
- **Departments** - Computer Science, Business, Engineering, etc.
- **Courses** - Programming, Web Development, Data Science, Marketing, etc.
- **Fees & Payment** - Tuition, hostel, library fees
- **Library** - Opening hours, available resources, computer labs
- **Placement** - Average package, placement percentage, top companies
- **Attendance** - Rules, minimum percentage, medical leave policy
- **Campus Facilities** - Sports, gym, cafeteria, medical center, etc.
- **Events** - Annual sports day, college fest, workshops, guest lectures

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (get free $5 credit at https://platform.openai.com)

### Setup (2 minutes)

1. **Add API Key**
   ```
   # Edit .env file and replace:
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

2. **Install Packages**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run Server**
   ```powershell
   python app.py
   ```

4. **Open Browser**
   ```
   http://127.0.0.1:5000
   ```

## 📁 Project Structure

```
college-assitant-chatbot/
├── app.py                    # Flask backend with OpenAI integration
├── requirements.txt          # Python dependencies
├── .env                      # API key (create from .env.example)
├── SETUP_GUIDE.md           # Detailed setup instructions
│
├── data/
│   ├── college_data.json    # College information database
│   ├── chat_db.py           # SQLite database module
│   └── chatbot.db           # SQLite database file (auto-created)
│
├── templates/
│   └── index.html           # Chatbot UI
│
└── static/
    ├── style.css            # Styling
    └── script.js            # Frontend logic
```

## 🎯 How It Works

1. **Student asks a question** in the chat interface
2. **Frontend sends to backend** via `/api/chat` endpoint
3. **Backend prepares context** with college data and chat history
4. **OpenAI API processes** the question with system instructions
5. **Response is returned** and displayed in the chat
6. **Conversation is saved** to SQLite database

## 💻 Code Examples

### Asking a Question (JavaScript)
```javascript
async function sendMessage() {
    const response = await fetch("/api/chat", {
        method: "POST",
        body: JSON.stringify({
            question: "What are the admission fees?",
            student_name: "John",
            conversation_history: [...]
        })
    });
    const data = await response.json();
    console.log(data.response); // AI response
}
```

### Backend Processing (Python)
```python
@app.route("/api/chat", methods=["POST"])
def chat():
    question = request.json.get("question")
    
    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": create_system_prompt()},
            {"role": "user", "content": question}
        ]
    )
    
    answer = response.choices[0].message.content
    save_chat(student_name, question, answer)
    return jsonify({"response": answer})
```

## 🎓 Learning Outcomes

By studying this project, you'll learn:

### Python
- Variables and data types
- Functions and decorators
- Exception handling
- File I/O (JSON, SQLite)
- Working with external APIs

### Flask
- Creating routes and endpoints
- Handling POST/GET requests
- JSON serialization
- Error handling

### JavaScript
- Async/await and Promises
- Fetch API
- DOM manipulation
- Event handling
- String formatting

### Frontend
- HTML structure
- CSS flexbox layout
- Responsive design
- Animations and transitions

## 🔐 Security Notes

⚠️ **API Key Protection:**
- Never commit `.env` to git
- Don't share your API key
- Use `.gitignore` to exclude sensitive files
- Regenerate key if accidentally exposed

⚠️ **Frontend Safety:**
- API key is stored server-side only
- Frontend never sees the actual API key
- HTML sanitization prevents XSS attacks

## 📊 Database Schema

### chat_history table
```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    question TEXT,
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: No module named 'flask'" | Run `pip install -r requirements.txt` |
| "API key not configured" | Add valid key to `.env` file |
| "Port 5000 already in use" | Change port in app.py line 127 |
| "Cannot find college_data.json" | Check file path in `data/` folder |

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed troubleshooting.

## 🚀 Future Enhancements

- [ ] User authentication
- [ ] Multiple language support
- [ ] File upload for documents
- [ ] Admin panel for data management
- [ ] Chatbot training with custom data
- [ ] Mobile app (React Native/Flutter)
- [ ] Voice input/output
- [ ] Analytics dashboard

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask server with API endpoints |
| `requirements.txt` | Python package dependencies |
| `.env` | Environment variables (API key) |
| `data/college_data.json` | Sample college information |
| `data/chat_db.py` | SQLite database functions |
| `templates/index.html` | HTML chatbot interface |
| `static/style.css` | CSS styling |
| `static/script.js` | JavaScript frontend logic |

## 📚 Resources

- **Flask Docs:** https://flask.palletsprojects.com/
- **OpenAI API:** https://platform.openai.com/docs/
- **Python Guide:** https://docs.python.org/3/
- **JavaScript:** https://developer.mozilla.org/en-US/docs/Web/JavaScript/

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💼 Author

Created as a learning project for Python, Flask, and AI integration.

---

**Ready to get started?** See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions!

**Have questions?** Check the comments in the code - every function is explained!

🎉 Happy learning and building!
