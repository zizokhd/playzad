from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, Application, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler
import os
#token bot

TOKEN = os.getenv("TOKEN")

ADMIN_ID = 7462244340
 
products = {

    "Box : ps4 + 2 controller + 3 dvd games":" ملاين 5 ",
    "Box : 2controller + 3 dvd games":"3 ملاين",
    "dvd games more":"450 الف"
}

#امر البدء start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.chat_data.clear()
    buttons = [
        ["المنتجات🛒","طلب"],
        ["مساعدة"]
        
    ]
    keyboard = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
    
    await update.message.reply_text(
        "مرحبا بك في متجرنا ☺️",reply_markup=keyboard
    )
    return ConversationHandler.END
async def rest_order(update: Update,context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
# التعامل مع أزرار القائمة
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
     
    if text == "المنتجات🛒":
        keyboard = [
            [InlineKeyboardButton("Box : ps4 + 2 controller + 3 dvd games", callback_data="box pro")],
            [InlineKeyboardButton("Box : 2controller + 3 dvd games", callback_data="box minaul")],
            [InlineKeyboardButton("Box : dvd games more", callback_data="box game")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = "المنتجات المتوفرة :\n\n"
         
            
        await update.message.reply_text(
            msg,
            reply_markup=reply_markup
        )
    elif text == "مساعدة":
        await update.message.reply_text(
        "دليل استخدام البوت🤖\n\n"
        "مرحبًا بك في متجرنا 🛍\n\n"
        "طريقة استخدام البوت:\n"
        "1- اضغط زر (المنتجات) لمشاهدة المنتجات المتوفرة.\n"
        "2- اضغط زر (طلب) لبدء طلب جديد.\n"
        "3- أدخل معلوماتك بالترتيب:\n"
        "   • الاسم الكامل\n"
        "   • رقم الهاتف\n"
        "   • الولاية\n"
        "   • العنوان\n"
        "4- اختر المنتج الذي تريده.\n"
        "5- سيتم إرسال طلبك مباشرة للإدارة ✅\n\n"
        "6- لي الغاء الطلب اكتب /cancel ❌\n"
        "ملاحظة:\n"
        "رقم الهاتف يجب أن يكون 10 أرقام ويبدأ بـ 05 أو 06 أو 07.\n\n"
        
    )
    
        

        #اسعار المنتجات
async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "box pro":
        await query.message.reply_text("5 ملاين 💵")
    if query.data == "box minaul":
        await query.message.reply_text("3 ملاين 💵")
    if query.data == "box game":
        await query.message.reply_text("450 الف 💵")


 
      

NAME, PHONE, STATE, ADDRESS, PRODUCT = range(5)

#بدء الطلب
async def start_order(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اسمك الكامل :",reply_markup=ReplyKeyboardRemove())
    return NAME

async def get_name(update: Update,context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("رقم هاتفك :")
    return PHONE
async def get_phone(update: Update,context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("الولاية")
    return STATE
async def get_state(update: Update,context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = update.message.text
    await update.message.reply_text("العنوان :")
    return ADDRESS

async def get_address(update: Update,context: ContextTypes.DEFAULT_TYPE):
    context.user_data["address"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Box : ps4 + 2 controller + 3 dvd games", callback_data="box pro")],
        [InlineKeyboardButton("Box : 2controller + 3 dvd games", callback_data="box minaul")],
        [InlineKeyboardButton("Box : dvd games more", callback_data="box game")]
    ]
    msg2 = "اختر المنتج 😊"
    await update.message.reply_text(
        msg2,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRODUCT

async def cancel_order(update: Update,context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    buttons = [
        ["المنتجات🛒","طلب"],
        ["مساعدة"]
         
    ]
    keyboard = ReplyKeyboardMarkup(buttons,resize_keyboard=True)
    await update.message.reply_text(
        "تم الغاء الطلب ❌",
        reply_markup=keyboard
    )
    return ConversationHandler.END

    

async def get_product(update: Update,context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    product_name = query.data
    context.user_data["product"] = product_name
    buttons = [
        ["المنتجات🛒","الطلب"],
        ["مساعدة"]
        
        ]
    keyboard = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
        )
    order_text = f"""

        طلب جديد 💴💵💰
        
        الاسم : {context.user_data["name"]}
        الهاتف : {context.user_data["phone"]}
        الولاية : {context.user_data["state"]}
        العنوان : {context.user_data["address"]}
        المنتج : {context.user_data["product"]}
    """
 
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=order_text)
    await query.message.reply_text(
        "تم ارسال طلبك بنجاح ✅",
        reply_markup = keyboard
        )
    
    return ConversationHandler.END



app = Application.builder().token(TOKEN).build()


conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.TEXT & filters.Regex("طلب"), start_order)
    ],
    states = {
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_state)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        PRODUCT: [CallbackQueryHandler(get_product)]
    },
    
    fallbacks=[
        CommandHandler("start",start),
        CommandHandler("cancel", cancel_order),
         
    ],
        allow_reentry=True
)


app.add_handler(CommandHandler("start",start))
app.add_handler(conv_handler)
app.add_handler(MessageHandler(filters.TEXT, menu))
app.add_handler(CallbackQueryHandler(prices))

app.run_polling()
