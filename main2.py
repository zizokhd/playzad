from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
import os

TOKEN = "8595403205:AAF8P58SUEO1pNw1sWRvftAG3dnFXjvx-uk"  # 🔐 التوكن من Render
ADMIN_ID = 7462244340  # 🔴 حط رقمك هنا

forbidden_buttons = [
    "📦 عرض المنتجات",
    "💰 الأسعار",
    "📝 طلب",
    "📊 احصائيات",
    "🔙 رجوع",
    "box : ps4 + 2 controller + 3 dvd games",
    "box : 2 controller + 3 dvd games",
    "dvd gamese more"
] 

# 📁 ملف البيانات
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "orders": 0}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# 🧠 تخزين الطلبات المؤقت
user_data = {}

 
# 🎛️ قائمة الزبون
user_menu = ReplyKeyboardMarkup(
    [["📦 عرض المنتجات"], ["📝 طلب"]],
    resize_keyboard=True
)

# 🔐 قائمة المدير
admin_menu = ReplyKeyboardMarkup(
    [["📦 عرض المنتجات"], ["📝 طلب"], ["📊 احصائيات"]],
    resize_keyboard=True
)

# 📦 المنتجات
products_menu = ReplyKeyboardMarkup(
    [
        ["box : ps4 + 2 controller + 3 dvd games"],
        ["box : 2 controller + 3 dvd games"],
        ["dvd gamese more"],
        ["Back"]
    ],
    resize_keyboard=True
)

# 💰 الأسعار
products = {
    "box : ps4 + 2 controller + 3 dvd games": "💰 5 ملاين ومتين الف",
    "box : 2 controller + 3 dvd games": "💰 3 ملاين ونص",
    "dvd gamese more": "💰 450 الف"
}

# 🚀 start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_id not in data["users"]:
        data["users"].append(user_id)
        save_data(data)

    # 👇 يحدد القائمة حسب الشخص
    if user_id == ADMIN_ID:
        menu = admin_menu
    else:
        menu = user_menu

    await update.message.reply_text(
        "هلا 👋 مرحبًا في متجر PLAYZAD 🎮",
        reply_markup=menu
    )

# 💬 التعامل
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.chat_id

    # 🔙 رجوع
    if text == "Back":
        if user_id in user_data:
            del user_data[user_id]

        if user_id == ADMIN_ID:
            menu = admin_menu
        else:
            menu = user_menu

        await update.message.reply_text(
            "رجعناك للقائمة الرئيسية 👇",
            reply_markup=menu
        )
        return

    # 📦 عرض المنتجات
    if text == "📦 عرض المنتجات":
        await update.message.reply_text(
            "اختر المنتج 👇",
            reply_markup=products_menu
        )

   

  
    elif text == "📊 احصائيات":
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ هذا الأمر غير متاح")
            return

        total_users = len(data["users"])
        total_orders = data["orders"]

        await update.message.reply_text(
            f"📊 الإحصائيات:\n"
            f"👥 الزبائن: {total_users}\n"
            f"🛒 الطلبات: {total_orders}"
        )

    

    # 📝 بدء الطلب
    elif text == "📝 طلب":
        user_data[user_id] = {"step": "name"}
        await update.message.reply_text("اكتب اسمك الكامل:")

   # 📝 بدء الطلب
    elif text == "📝 طلب":
        user_data[user_id] = {"step": "name"}
        await update.message.reply_text("اكتب اسمك الكامل:")
        return

# 🧠 خطوات الطلب (لازم تكون فوق عرض السعر!)
    elif user_id in user_data:

        step = user_data[user_id]["step"]

        # ❌ منع الأزرار أثناء إدخال البيانات (إلا في اختيار المنتج)
        if step != "product" and text in forbidden_buttons:
            await update.message.reply_text("❌ اكتب البيانات المطلوبة فقط، لا تستخدم الأزرار الآن")
            return

        # 👤 الاسم
        if step == "name":
            name = text.strip()

            # تحقق الاسم
            if not name.replace(" ", "").isalpha():
                await update.message.reply_text("❌ الاسم لازم يكون حروف فقط")
                return

            if len(name) < 3 or len(name) > 20:
                await update.message.reply_text("❌ الاسم لازم يكون بين 3 و 20 حرف")
                return

            user_data[user_id]["name"] = name
            user_data[user_id]["step"] = "phone"

            await update.message.reply_text("📱 اكتب رقم هاتفك:")
            return

        # 📱 الهاتف
        elif step == "phone":
            phone = text.strip()

            if not phone.isdigit():
                await update.message.reply_text("❌ رقم الهاتف لازم يكون أرقام فقط")
                return

            if len(phone) != 10:
                await update.message.reply_text("❌ رقم الهاتف لازم يكون 10 أرقام بالضبط")
                return

            if not (phone.startswith("05") or phone.startswith("06") or phone.startswith("07")):
                await update.message.reply_text("❌ رقم الهاتف لازم يبدأ بـ 05 أو 06 أو 07")
                return

            user_data[user_id]["phone"] = phone
            user_data[user_id]["step"] = "state"

            await update.message.reply_text("📍 اكتب ولايتك:")
            return

        # 📍 الولاية
        elif step == "state":
            state = text.strip()

            if len(state) < 3:
                await update.message.reply_text("❌ اكتب ولاية صحيحة")
                return

            user_data[user_id]["state"] = state
            user_data[user_id]["step"] = "address"

            await update.message.reply_text("🏠 اكتب عنوانك:")
            return

        # 🏠 العنوان
        elif step == "address":
            address = text.strip()

            if len(address) < 5:
                await update.message.reply_text("❌ اكتب عنوان أوضح")
                return

            user_data[user_id]["address"] = address
            user_data[user_id]["step"] = "product"

            await update.message.reply_text(
                "🛒 اختر المنتج:",
                reply_markup=products_menu
            )
            return

        # 🛒 اختيار المنتج
        elif step == "product":

            if text not in products:
                await update.message.reply_text("❌ اختر من القائمة فقط")
                return

            user_data[user_id]["product"] = text
            order = user_data[user_id]

            # 📊 تحديث الطلبات
            data["orders"] += 1
            save_data(data)

            message = f"""
    📦 طلب جديد!

    👤 الاسم: {order['name']}
    📱 الهاتف: {order['phone']}
    📍 الولاية: {order['state']}
    🏠 العنوان: {order['address']}
    🛒 المنتج: {order['product']}
    """

            await context.bot.send_message(chat_id=ADMIN_ID, text=message)

            await update.message.reply_text("✅ تم إرسال طلبك بنجاح!")

            del user_data[user_id]
            return
        
    elif text in products:
            await update.message.reply_text(products[text])
# 🚀 تشغيل
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()