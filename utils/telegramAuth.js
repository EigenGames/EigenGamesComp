// utils/telegramAuth.js
const crypto = require("crypto");

function checkTelegramAuth(dataObj, botToken) {
  const { hash, ...dataCheckArr } = dataObj;
  const sorted = Object.keys(dataCheckArr)
    .sort()
    .map(key => `${key}=${dataCheckArr[key]}`)
    .join("\n");
  const secretKey = crypto.createHash("sha256").update(botToken).digest();
  const hmac = crypto.createHmac("sha256", secretKey).update(sorted).digest("hex");
  return hmac === hash;
}

module.exports = { checkTelegramAuth };
