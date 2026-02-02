import telebot
from flask import Flask
from threading import Thread
import os

# 1. Web Server එක සෙට් කිරීම (බොට්ව පණගන්වා තැබීමට)
app = Flask('')


@app.route('/')
def home():
    return "MyDenoBot is Alive and Running!"


def run():
    # Render හෝ Replit සඳහා Port එක ලබාගැනීම
    # මෙතන default පෝර්ට් එක 10000 ලෙස දමා ඇත
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()


# 2. Telegram Bot එකේ තොරතුරු (ඔයාගේ API TOKEN එක මෙතන තියෙනවා)
API_TOKEN = '8535970339:AAG8UZn1_VpeRVgKqE_2gzlETRyqzd1hf7M'
bot = telebot.TeleBot(API_TOKEN)


# /start command එකට ලැබෙන පිළිතුර
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("👋 ආයුබෝවන් අමිත්!\n\n"
                    "ගණනය කිරීම් සිදු කිරීමට අගයන් දෙකක් එවන්න.\n"
                    "උදාහරණ: `10 20` (Labeling සඳහා 10, Verification සඳහා 20)")
    bot.reply_to(message, welcome_text, parse_mode='Markdown')


# අංක ලැබුණු විට ගණනය කිරීම සිදු කරන කොටස
@bot.message_handler(func=lambda message: True)
def calculate_deno(message):
    try:
        # මැසේජ් එකේ තියෙන අංක දෙක වෙන් කර ගැනීම
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "⚠️ කරුණාකර අංක දෙකක් එවන්න. (උදා: 10 20)")
            return

        l_count = float(parts[0])
        v_count = float(parts[1])

        # ගණනය කිරීම් (ඔයා දුන් අගයන් අනුව)
        l_total = l_count * 1.83
        v_total = v_count * 2.63
        grand_total = l_total + v_total

        response = (f"📊 *Deno Summary*\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🏷️ Labeling: *{l_total:.2f}*\n"
                    f"✅ Verification: *{v_total:.2f}*\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💰 *Total: {grand_total:.2f}*")
        bot.reply_to(message, response, parse_mode='Markdown')

    except ValueError:
        bot.reply_to(message, "❌ වැරදියි! කරුණාකර අංක පමණක් භාවිතා කරන්න.")
    except Exception as e:
        bot.reply_to(message, "⚠️ යම් දෝෂයක් සිදු විය. පසුව උත්සාහ කරන්න.")


# 3. බොට්ව ක්‍රියාත්මක කිරීම
if __name__ == "__main__":
    keep_alive()  # Web Server එක පණගැන්වීම
    print("MyDenoBot is starting...")
    bot.infinity_polling()
