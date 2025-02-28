import telebot
import json
import os
import openai
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Missing required API keys! Check .env file.")

# ✅ Initialize Telegram Bot & OpenAI Client (OLD WORKING FORMAT)
bot = telebot.TeleBot(BOT_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)  # 🔄 Reverted API call to working version

# ✅ File paths for storing agent requests & groups
AGENT_REQUESTS_FILE = "agent_requests.json"
DEPLOYED_AGENTS_FILE = "deployed_agents.json"
USER_GROUPS_FILE = "user_groups.json"

# ✅ Load and save JSON data
def load_data(filename, default_data=None):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_data or {}, f)
    with open(filename, "r") as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# ✅ Load existing data
agent_requests = load_data(AGENT_REQUESTS_FILE, default_data={})
deployed_agents = load_data(DEPLOYED_AGENTS_FILE, default_data={})
user_groups = load_data(USER_GROUPS_FILE, default_data={})

# ✅ Start Message
@bot.message_handler(commands=["start"])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "🚀 WOTBRAIN_bot HERE! No Brakes, 100% Execution!\n\nTell me what you're looking for, and I'll figure out how to help!")
    user_state[chat_id] = "waitingForInput"

# ✅ Corrected OpenAI API Call (Using Old Working Version)
def analyze_intent_and_extract_details(user_text):
    prompt = f"""
    The user sent the following message:
    "{user_text}"

    Determine whether this is:
    - A casual conversation ("chat")
    - A request for an AI Agent ("ai_request")
    - A request to join a group ("group_request")

    Also, extract any key user details such as their profession, interests, or specific task.

    Return JSON like this:
    {{"intent": "ai_request", "user_details": ["preschool teacher", "flashcards"]}}
    """

    try:
        response = client.chat.completions.create(  # ✅ REVERTED TO WORKING FORMAT
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an AI that categorizes user requests."},
                      {"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )

        response_content = response.choices[0].message.content  # ✅ Fix API response handling

        try:
            return json.loads(response_content)  # ✅ Ensure JSON parsing
        except json.JSONDecodeError:
            print(f"⚠️ JSON Parsing Error! OpenAI Output:\n{response_content}")
            return {"intent": "chat", "user_details": []}  # Default to chat mode

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return {"intent": "chat", "user_details": []}  # Fail gracefully

# ✅ Handle messages dynamically
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_text = message.text

    # 🔹 Step 1: Determine Intent
    analysis = analyze_intent_and_extract_details(user_text)
    intent = analysis["intent"]
    user_details = analysis["user_details"]

    # 🔹 Step 2: Handle Intent
    if intent == "chat":
        bot.send_message(chat_id, f"🤖 [AI Response]: \"{user_text}\"")  # Simple chat response
    
    elif intent == "ai_request":
        process_agent_request(chat_id, user_text, user_details)

    elif intent == "group_request":
        assign_user_to_group(chat_id, user_details)
    
    else:
        bot.send_message(chat_id, "❓ Not sure what you mean, but let's chat!")

# ✅ AI Agent Processing
def process_agent_request(chat_id, user_task, user_details):
    matched_agent = match_existing_agent(user_task)

    if matched_agent != "No match found":
        bot.send_message(chat_id, f"📂 I found an existing AI Agent that may help: {matched_agent}")
        return

    # Ask user if they want an agent built
    bot.send_message(chat_id, f"🚀 No pre-built agent found! Should I build one for you?")
    user_state[chat_id] = {"state": "confirming_agent_request", "task": user_task, "details": user_details}

# ✅ AI Agent Confirmation
@bot.message_handler(func=lambda message: user_state.get(message.chat.id, {}).get("state") == "confirming_agent_request")
def confirm_agent_request(message):
    chat_id = message.chat.id
    response = message.text.lower()

    if "yes" in response or "sure" in response:
        task_details = user_state[chat_id]["task"]
        save_agent_request(chat_id, task_details)
        bot.send_message(chat_id, f"✅ Your AI Agent request for '{task_details}' has been saved! 🚀 We'll notify you when it's built.")
    else:
        bot.send_message(chat_id, "👍 No worries! Let me know if you need something else.")

    del user_state[chat_id]  # Reset state

# ✅ Save AI Agent Requests
def save_agent_request(chat_id, user_task):
    agent_requests[str(chat_id)] = user_task
    save_data(AGENT_REQUESTS_FILE, agent_requests)

# ✅ AI Agent Matching
def match_existing_agent(user_task):
    # 🔍 First, check if an exact agent is in our stored deployed_agents.json
    for agent_name in deployed_agents.keys():
        if agent_name.lower() in user_task.lower():
            return agent_name  # ✅ Return the existing agent if found

    # 🧠 If no exact match, ask OpenAI to match similar agents
    prompt = f"""
    Given the user request: "{user_task}", check if it aligns with any of these deployed AI agents: {list(deployed_agents.keys())}.
    If there's a match, return ONLY the agent name.
    If no match exists, return "No match found".
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are an AI that finds the best existing AI agent for a user request."},
                      {"role": "user", "content": prompt}],
            max_tokens=50,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ OpenAI Matching Error: {e}")
        return "No match found"


# ✅ Assign Users to Interest-Based Groups
def assign_user_to_group(chat_id, user_interest):
    interest_group = user_interest[0] if user_interest else "General"

    if interest_group in user_groups:
        user_groups[interest_group].append(chat_id)
    else:
        user_groups[interest_group] = [chat_id]

    save_data(USER_GROUPS_FILE, user_groups)
    bot.send_message(chat_id, f"✅ You've been added to the **{interest_group}** group!")

# ✅ Start Bot
if __name__ == "__main__":
    print("🤖 WOTBRAIN Telegram Bot is running...")
    user_state = {}  # Store user conversation state
    bot.polling()
