from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OpenAI API Key is missing! Check your .env file.")

# ✅ Initialize OpenAI client (NEW FORMAT)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_prompt = data.get("text", "")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # ✅ Updated API call for OpenAI v1.0+
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=100
        )

        bot_response = response.choices[0].message.content
        return jsonify({"text": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
