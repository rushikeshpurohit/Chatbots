from flask import Flask, request, render_template, jsonify
from groq import Groq
import random

app = Flask(__name__)

# 🔐 Replace with your real Groq API key
client = Groq(api_key="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")

# 🎉 Fun emoji stickers for responses
stickers = ["🤖", "😊", "🔥", "🎉", "💡", "🚀", "✨", "📚", "😎"]

# 💬 Initial system message to guide the assistant (now focused on coding/CS help)
messages = [
    {
        "role": "system",
        "content": (
            "You are rishi, an expert technical assistant specializing in computer science, "
            "programming, software engineering, algorithms, and related technologies. "
            "You help users with coding problems, debugging, explanations, and technical concepts. "
            "Always provide clear, structured explanations with examples when useful. "
            "Detect the user's language and respond in the same language. "
            "If the language is mixed, respond in the primary language of the question."
        )
    }
]

# 🌐 Home route serving the chatbot UI
@app.route("/")
def home():
    return render_template("index.html")

# 📡 Endpoint to handle chat messages from frontend
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message received."}), 400

    # Add user message to conversation history
    messages.append({"role": "user", "content": user_input})

    try:
        # Call Groq LLM API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile"  # ⚡ still the same model
        )

        # Extract the reply from the assistant
        reply = chat_completion.choices[0].message.content

        # Add assistant reply to history
        messages.append({"role": "assistant", "content": reply})

        # Send back reply and random sticker
        return jsonify({
            "reply": reply,
            "sticker": random.choice(stickers)
        })

    except Exception as e:
        # Handle API or network issues
        return jsonify({
            "error": "Something went wrong. Please try again.",
            "details": str(e)
        }), 500

# 🚀 Run the app
if __name__ == "__main__":
    app.run(debug=True)
