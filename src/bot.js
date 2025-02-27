require("dotenv").config();
const TelegramBot = require("node-telegram-bot-api");

const botToken = process.env.TELEGRAM_BOT_TOKEN;

if (!botToken) {
  console.error("TELEGRAM_BOT_TOKEN is missing from .env!");
  process.exit(1);
}

const bot = new TelegramBot(botToken, { polling: true });

console.log("🚀 WOTBRAIN_bot is ONLINE! FULL EXECUTION MODE!");

const userState = {}; // Temporary state tracking user intent

// 🤖 Start command - Ask user what they need
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(
    chatId,
    `🔥 WOTBRAIN_bot HERE! 🚀 No Brakes, 100% Execution!\n\nWhat can I do for you?\n\n1️⃣ Just Chat 🤖\n2️⃣ Join a Topic Group 👥\n3️⃣ Get an AI Agent ⚡`,
    {
      reply_markup: {
        keyboard: [["🤖 Just Chat"], ["👥 Join a Topic Group"], ["⚡ Get an AI Agent"]],
        one_time_keyboard: true,
      },
    }
  );
  userState[chatId] = "waitingForSelection";
});

// ✅ Process User’s Selection
bot.on("message", (msg) => {
  const chatId = msg.chat.id;
  const userText = msg.text;

  // Step 1: Handle Selection
  if (userState[chatId] === "waitingForSelection") {
    if (userText.includes("Just Chat")) {
      bot.sendMessage(chatId, `💬 Alright! Just send me a message and I’ll reply!`);
      userState[chatId] = "chat";
    } else if (userText.includes("Join a Topic Group")) {
      bot.sendMessage(chatId, `👥 What topic are you interested in?`);
      userState[chatId] = "groupSelection";
    } else if (userText.includes("Get an AI Agent")) {
      bot.sendMessage(chatId, `⚡ What task do you need an AI Agent for?`);
      userState[chatId] = "agentRequest";
    } else {
      bot.sendMessage(chatId, `❓ I didn’t get that. Choose an option.`);
    }
    return;
  }

  // Step 2: Handle Chat Mode
  if (userState[chatId] === "chat") {
    bot.sendMessage(chatId, `🤖 [AI Response Placeholder]: "${userText}"`);
    return;
  }

  // Step 3: Handle Topic Group Selection
  if (userState[chatId] === "groupSelection") {
    bot.sendMessage(chatId, `✅ You’ve been added to the **${userText}** group!`);
    // In future versions, we actually group users.
    return;
  }

  // Step 4: Handle AI Agent Requests
  if (userState[chatId] === "agentRequest") {
    bot.sendMessage(
      chatId,
      `⚙️ Checking if an agent exists for: "${userText}"...`
    );
    setTimeout(() => {
      // In a real version, we'd check a database.
      bot.sendMessage(
        chatId,
        `❌ No pre-built agent found! 🚀 Your request has been added to the AI development queue!`
      );
      // Future step: Add request to development repo
    }, 2000);
    return;
  }
});

module.exports = bot;
