// ==========================================================
// COLLEGE ASSISTANT - SCRIPT.JS
// Chatbot + College Data
// ==========================================================


// ==========================================================
// GLOBAL VARIABLES
// ==========================================================

let conversationHistory = [];
let collegeData = null;


// ==========================================================
// GET HTML ELEMENTS
// ==========================================================

const questionInput =
    document.getElementById("questionInput");

const sendButton =
    document.getElementById("sendButton");

const messagesContainer =
    document.getElementById("messagesContainer");

const studentNameInput =
    document.getElementById("studentName");

const charCountDisplay =
    document.getElementById("charCount");

const clearChat =
    document.getElementById("clearChat");


// ==========================================================
// LOAD COLLEGE DATA
// ==========================================================

async function loadCollegeData() {

    try {

        const response =
            await fetch("/api/college-data");

        if (!response.ok) {

            throw new Error(
                "Unable to load college data"
            );
        }

        const data =
            await response.json();

        if (data.error) {

            throw new Error(
                data.error
            );
        }

        collegeData = data;

        console.log(
            "College data loaded:",
            collegeData
        );


        // ==================================================
        // UPDATE COLLEGE NAME
        // ==================================================

        const collegeName =
            document.getElementById(
                "collegeName"
            );

        if (
            collegeName &&
            data.college_name
        ) {

            collegeName.textContent =
                data.college_name;
        }


    } catch (error) {

        console.error(
            "College data error:",
            error
        );

        showError(
            "College information could not be loaded."
        );
    }
}


// ==========================================================
// CHARACTER COUNT
// ==========================================================

if (questionInput) {

    questionInput.addEventListener(
        "input",
        function () {

            if (charCountDisplay) {

                charCountDisplay.textContent =
                    this.value.length;
            }
        }
    );
}


// ==========================================================
// ENTER KEY
// ==========================================================

if (questionInput) {

    questionInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();
            }
        }
    );
}


// ==========================================================
// SEND BUTTON
// ==========================================================

if (sendButton) {

    sendButton.addEventListener(
        "click",
        sendMessage
    );
}


// ==========================================================
// SEND CHAT MESSAGE
// ==========================================================

async function sendMessage() {

    // ======================================================
    // PREVENT MULTIPLE CLICKS
    // ======================================================

    if (
        !sendButton ||
        sendButton.disabled
    ) {

        return;
    }


    // ======================================================
    // GET QUESTION
    // ======================================================

    const question =
        questionInput
            ? questionInput.value.trim()
            : "";


    // ======================================================
    // GET STUDENT NAME
    // ======================================================

    const studentName =
        studentNameInput &&
        studentNameInput.value.trim()
            ? studentNameInput.value.trim()
            : "Student";


    // ======================================================
    // EMPTY QUESTION
    // ======================================================

    if (!question) {

        showError(
            "Please enter a question."
        );

        return;
    }


    // ======================================================
    // MAXIMUM QUESTION LENGTH
    // ======================================================

    if (question.length > 500) {

        showError(
            "Question is too long. Maximum 500 characters."
        );

        return;
    }


    // ======================================================
    // DISABLE SEND BUTTON
    // ======================================================

    sendButton.disabled = true;

    sendButton.innerHTML =
        '<span>Sending...</span>';


    // ======================================================
    // SHOW STUDENT MESSAGE
    // ======================================================

    addChatMessage(
        question,
        "student"
    );


    // ======================================================
    // CLEAR INPUT
    // ======================================================

    if (questionInput) {

        questionInput.value = "";
    }


    // ======================================================
    // RESET CHARACTER COUNT
    // ======================================================

    if (charCountDisplay) {

        charCountDisplay.textContent = "0";
    }


    // ======================================================
    // ADD USER MESSAGE TO HISTORY
    // ======================================================

    conversationHistory.push({

        role: "user",

        content: question
    });


    // ======================================================
    // SEND REQUEST TO BACKEND
    // ======================================================

    try {

        const response =
            await fetch(
                "/api/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question: question,

                        student_name:
                            studentName,

                        conversation_history:
                            conversationHistory
                    })
                }
            );


        // ==================================================
        // READ RESPONSE
        // ==================================================

        const data =
            await response.json();


        // ==================================================
        // CHECK RESPONSE
        // ==================================================

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );
        }


        // ==================================================
        // GET BOT ANSWER
        // ==================================================

        const answer =
            data.response ||
            data.answer ||
            data.reply;


        if (!answer) {

            throw new Error(
                "No response received."
            );
        }


        // ==================================================
        // SHOW BOT RESPONSE
        // ==================================================

        addChatMessage(
            answer,
            "bot"
        );


        // ==================================================
        // ADD ASSISTANT RESPONSE TO HISTORY
        // ==================================================

        conversationHistory.push({

            role: "assistant",

            content: answer
        });


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        showError(
            error.message ||
            "Unable to get response."
        );
    }


    // ======================================================
    // ENABLE SEND BUTTON
    // ======================================================

    sendButton.disabled = false;

    sendButton.innerHTML =
        '<span class="send-text">Send</span>' +
        '<span class="send-icon">➤</span>';
}


// ==========================================================
// ADD CHAT MESSAGE
// ==========================================================

function addChatMessage(
    text,
    sender
) {

    if (!messagesContainer) {

        return;
    }


    // ======================================================
    // MESSAGE CONTAINER
    // ======================================================

    const messageDiv =
        document.createElement("div");


    // ======================================================
    // STUDENT / BOT CLASS
    // ======================================================

    messageDiv.className =
        sender === "student"
            ? "message student-message"
            : "message bot-message";


    // ======================================================
    // MESSAGE CONTENT
    // ======================================================

    const contentDiv =
        document.createElement("div");


    contentDiv.className =
        "message-content";


    // ======================================================
    // SAFE MESSAGE PARSING
    // ======================================================

    contentDiv.innerHTML =
        parseMessage(text);


    // ======================================================
    // TIMESTAMP
    // ======================================================

    const timestamp =
        document.createElement("span");


    timestamp.className =
        "timestamp";


    timestamp.textContent =
        getCurrentTime();


    // ======================================================
    // APPEND MESSAGE
    // ======================================================

    messageDiv.appendChild(
        contentDiv
    );

    messageDiv.appendChild(
        timestamp
    );


    // ======================================================
    // ADD TO CHAT
    // ======================================================

    messagesContainer.appendChild(
        messageDiv
    );


    // ======================================================
    // SCROLL TO BOTTOM
    // ======================================================

    scrollToBottom();
}


// ==========================================================
// ERROR MESSAGE
// ==========================================================

function showError(message) {

    if (!messagesContainer) {

        return;
    }


    const errorDiv =
        document.createElement("div");


    errorDiv.className =
        "message bot-message";


    const content =
        document.createElement("div");


    content.className =
        "message-content error-message";


    content.textContent =
        "❌ " + message;


    errorDiv.appendChild(
        content
    );


    messagesContainer.appendChild(
        errorDiv
    );


    scrollToBottom();
}


// ==========================================================
// PARSE CHAT MESSAGE
// ==========================================================

function parseMessage(text) {

    // ======================================================
    // CONVERT TO STRING
    // ======================================================

    let safeText =
        String(text);


    // ======================================================
    // ESCAPE HTML
    // ======================================================

    safeText =
        safeText
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");


    // ======================================================
    // BOLD
    // Example: **Hello**
    // ======================================================

    safeText =
        safeText.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    // ======================================================
    // ITALIC
    // Example: *Hello*
    // ======================================================

    safeText =
        safeText.replace(
            /\*(.*?)\*/g,
            "<em>$1</em>"
        );


    // ======================================================
    // NEW LINE
    // ======================================================

    safeText =
        safeText.replace(
            /\n/g,
            "<br>"
        );


    return safeText;
}


// ==========================================================
// CURRENT TIME
// ==========================================================

function getCurrentTime() {

    const now =
        new Date();


    const hours =
        String(
            now.getHours()
        ).padStart(
            2,
            "0"
        );


    const minutes =
        String(
            now.getMinutes()
        ).padStart(
            2,
            "0"
        );


    return `${hours}:${minutes}`;
}


// ==========================================================
// SCROLL TO BOTTOM
// ==========================================================

function scrollToBottom() {

    if (!messagesContainer) {

        return;
    }


    messagesContainer.scrollTop =
        messagesContainer.scrollHeight;
}


// ==========================================================
// CLEAR CHAT
// ==========================================================

if (clearChat) {

    clearChat.addEventListener(
        "click",
        function () {


            // ==================================================
            // CLEAR CONVERSATION HISTORY
            // ==================================================

            conversationHistory = [];


            // ==================================================
            // CLEAR CHAT MESSAGES
            // ==================================================

            if (messagesContainer) {

                messagesContainer.innerHTML =
                    "";
            }


            // ==================================================
            // CLEAR COLLEGE INFORMATION
            // ==================================================

            const informationSection =
                document.getElementById(
                    "collegeInformation"
                );


            if (informationSection) {

                informationSection.innerHTML =
                    "";
            }


            // ==================================================
            // CLEAR QUESTION INPUT
            // ==================================================

            if (questionInput) {

                questionInput.value = "";
            }


            // ==================================================
            // RESET CHARACTER COUNT
            // ==================================================

            if (charCountDisplay) {

                charCountDisplay.textContent =
                    "0";
            }


            // ==================================================
            // FOCUS QUESTION INPUT
            // ==================================================

            if (questionInput) {

                questionInput.focus();
            }

        }
    );
}


// ==========================================================
// PAGE LOAD
// ==========================================================

window.addEventListener(
    "load",
    async function () {

        // ==================================================
        // LOAD COLLEGE DATA
        // ==================================================

        await loadCollegeData();


        // ==================================================
        // FOCUS QUESTION BOX
        // ==================================================

        if (questionInput) {

            questionInput.focus();
        }

    }
);