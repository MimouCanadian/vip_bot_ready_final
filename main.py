import telebot
import json
from config import TOKEN, ADMIN_ID, VIP_CHANNEL

bot = telebot.TeleBot(TOKEN)

PAYMENT_METHODS = ["paypal", "baridi", "usdt"]

@bot.message_handler(commands=['start'])
def start(message):
    text = '''🎓 مرحبًا بك في بوت الاشتراك VIP

اختر طريقة الدفع:
💳 PayPal - /paypal
📱 BaridiMob - /baridi
💸 USDT - /usdt

بعد الدفع، أرسل لنا إثبات الدفع (صورة أو نص).'''
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=PAYMENT_METHODS)
def send_payment_info(message):
    method = message.text[1:]
    if method == "paypal":
        response = "💳 ادفع 200$ إلى: mimoucanadien01@gmail.com"
    elif method == "baridi":
        response = "📱 أرسل 50000 دج إلى: 00799999001806537421"
    elif method == "usdt":
        response = "💸 أرسل 200 USDT إلى:\nTSG7N6P9XPVQudUtfFkjcmzi8VhMEmWyFr\nأو\nTSaMh2J3Ng3WbCZtyZizyycjhe2tciTnE2"
    bot.send_message(message.chat.id, response + "\nثم أرسل لنا إثبات الدفع هنا.")

@bot.message_handler(content_types=['text', 'photo'])
def handle_payment_proof(message):
    user_info = {
        "user_id": message.from_user.id,
        "name": message.from_user.first_name,
        "username": message.from_user.username,
        "payment_proof": message.text if message.text else "photo",
        "date": message.date
    }

    with open("data.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(user_info) + "\n")

    # إشعار المشرف
    msg = f"📩 تم استلام إثبات دفع من:\n👤 الاسم: {message.from_user.first_name}\n🧾 معرفه: @{message.from_user.username}\n\nهل تريد تأكيد الاشتراك؟"
    markup = telebot.types.InlineKeyboardMarkup()
    confirm_btn = telebot.types.InlineKeyboardButton("✅ تأكيد الاشتراك", callback_data=f"confirm:{message.chat.id}")
    markup.add(confirm_btn)

    if message.photo:
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=msg, reply_markup=markup)
    else:
        bot.send_message(ADMIN_ID, msg + f"\n💬 النص: {message.text}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm:"))
def confirm_subscription(call):
    user_id = call.data.split(":")[1]
    bot.send_message(user_id, f"✅ تم تأكيد الدفع! مرحبًا بك في قناة VIP.\n🔗 {VIP_CHANNEL}")
    bot.answer_callback_query(call.id, "تمت إضافة المستخدم.")

print("✅ Bot is running...")
bot.infinity_polling()