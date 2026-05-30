from flask import Flask, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

# ---------------- FAQ DATA ----------------
faqs = [
    {"question": "What is your return policy?", "answer": "You can return products within 7 days of delivery."},
    {"question": "How can I track my order?", "answer": "You can track your order using the tracking ID sent to your email."},
    {"question": "Do you offer cash on delivery?", "answer": "Yes, COD is available in selected areas."},
    {"question": "How long does delivery take?", "answer": "Delivery usually takes 3–7 business days."},
    {"question": "How can I contact support?", "answer": "You can contact support via email or helpline number."}
]

questions = [f["question"] for f in faqs]
answers = [f["answer"] for f in faqs]

# ---------------- NLP PREPROCESSING (SpaCy + cleaning) ----------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)

    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]

    return " ".join(tokens)

processed_questions = [preprocess(q) for q in questions]

# ---------------- TF-IDF MODEL ----------------
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_questions)

# ---------------- RESPONSE FUNCTION ----------------
def get_response(user_input):
    user_input = preprocess(user_input)
    user_vec = vectorizer.transform([user_input])

    similarity = cosine_similarity(user_vec, tfidf_matrix)
    idx = similarity.argmax()
    score = similarity[0][idx]

    if score < 0.2:
        return "Sorry, I couldn't find a relevant answer."

    return answers[idx]

# ---------------- HTML UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FAQ Chatbot</title>
    <style>
        body { font-family: Arial; background: #f2f2f2; }

        .container {
            width: 400px;
            margin: 50px auto;
            background: white;
            padding: 15px;
            border-radius: 10px;
        }

        .chat {
            height: 350px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
        }

        .user { text-align: right; color: blue; margin: 5px; }
        .bot { text-align: left; color: green; margin: 5px; }

        input {
            width: 70%;
            padding: 10px;
        }

        button {
            padding: 10px;
        }
    </style>
</head>
<body>

<div class="container">
    <h3>FAQ Chatbot 🤖</h3>

    <div class="chat" id="chat"></div>

    <input id="msg" placeholder="Ask your question..." />
    <button onclick="send()">Send</button>
</div>

<script>
function send(){
    let msg = document.getElementById("msg").value;
    if(msg.trim() === "") return;

    let chat = document.getElementById("chat");

    chat.innerHTML += "<div class='user'>You: " + msg + "</div>";

    fetch("/get", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "message=" + msg
    })
    .then(res => res.text())
    .then(data => {
        chat.innerHTML += "<div class='bot'>Bot: " + data + "</div>";
        chat.scrollTop = chat.scrollHeight;
    });

    document.getElementById("msg").value = "";
}
</script>

</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return HTML

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form["message"]
    return get_response(user_msg)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)