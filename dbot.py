import logging
from decouple import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

tk = config('token')
CHANNEL_ID = '@Taekwondo_irann'

VIDEO_URLS = {
    'olympic1': 'https://t.me/dgmhdkeyjagcomdmsatbt/18', #bagheri 2012
    'olympic2': 'https://t.me/dgmhdkeyjagcomdmsatbt/15', # karami 2012
    'olympic3': 'https://t.me/dgmhdkeyjagcomdmsatbt/17', # farzan 2016
    'olympic4': 'https://t.me/dgmhdkeyjagcomdmsatbt/16', # iran 2016
    'olympic5': 'https://t.me/dgmhdkeyjagcomdmsatbt/22', # mobina 2024-1
    'olympic6': 'https://t.me/dgmhdkeyjagcomdmsatbt/23', # mobina 2024-2
    'olympic7': 'https://t.me/dgmhdkeyjagcomdmsatbt/24', # mobina 2024-3
    'olympic8': 'https://t.me/dgmhdkeyjagcomdmsatbt/25', # mobina 2024-4
    'olympic9': 'https://t.me/dgmhdkeyjagcomdmsatbt/26', # nahid 2024-1
    'olympic10': 'https://t.me/dgmhdkeyjagcomdmsatbt/27', # nahid 2024-2
    'world1': 'https://t.me/dgmhdkeyjagcomdmsatbt/11', #  iran & rusia 2019
    'world2': 'https://t.me/dgmhdkeyjagcomdmsatbt/10', #  iran & china 2019
    'world3': 'https://t.me/dgmhdkeyjagcomdmsatbt/9', #  iran & brazil
    'grand1': 'https://t.me/dgmhdkeyjagcomdmsatbt/14', # yaghoobi & tazgul
    'grand2': 'https://t.me/dgmhdkeyjagcomdmsatbt/20', # mirhashem & day hon lee 2019
    'didani1': 'https://t.me/dgmhdkeyjagcomdmsatbt/13', # jam jahani 2019 chin
    'didani2': 'https://t.me/dgmhdkeyjagcomdmsatbt/12', # beigi 37 - 4
    'didani3': 'https://t.me/dgmhdkeyjagcomdmsatbt/21', # jj 2019 ND
    
}

def get_join_channel_button():
    keyboard = [[InlineKeyboardButton("عضویت در کانال دیموندو", url="https://t.me/Taekwondo_irann")],
                [InlineKeyboardButton("عضو شدم", callback_data='check_membership')]]
    return InlineKeyboardMarkup(keyboard)

def get_category_buttons():
    keyboard = [
        [InlineKeyboardButton("المپیک", callback_data='category_olympic')],
        [InlineKeyboardButton("جام جهانی", callback_data='category_world')],
        [InlineKeyboardButton("گرند پریکس", callback_data='category_grand')],
        [InlineKeyboardButton("دیدنی", callback_data='category_didani')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_video_buttons(category):
    keyboard = []
    if category == 'olympic':
        keyboard = [
            [InlineKeyboardButton("باقری معتمد & سروت تزگل *2012", callback_data='olympic1')],
            [InlineKeyboardButton("کرمی & گارسیا *2012", callback_data='olympic2')],
            [InlineKeyboardButton("عاشورزاده & حاجمی *2016", callback_data='olympic3')],
            [InlineKeyboardButton("بیگی & خدابخشی *2016", callback_data='olympic4')],
            [InlineKeyboardButton("نعمت زاده & تاو میشل *2024", callback_data='olympic5')],
            [InlineKeyboardButton("نعمت زاده & ایگلسیاس *2024", callback_data='olympic6')],
            [InlineKeyboardButton("نعمت زاده & گینگ گو *2024", callback_data='olympic7')],
            [InlineKeyboardButton("نعمت زاده: برنز *2024", callback_data='olympic8')],
            [InlineKeyboardButton("کیانی & علیزاده *2024", callback_data='olympic9')],
            [InlineKeyboardButton("کیانی & تومی *2024", callback_data='olympic10')],
            [InlineKeyboardButton("بازگشت", callback_data='back_to_categories')]
        ]
    elif category == 'world':
        keyboard = [
            [InlineKeyboardButton("تیم ترکیبی ایران & روسیه *2019", callback_data='world1')],
            [InlineKeyboardButton("تیم ترکیبی ایران & چین *2019", callback_data='world2')],
            [InlineKeyboardButton("تیم ترکیبی ایران & برزیل *2023", callback_data='world3')],
            [InlineKeyboardButton("بازگشت", callback_data='back_to_categories')]
        ]
    elif category == 'grand':
        keyboard = [
            [InlineKeyboardButton("یقوبی & تزگل *2016", callback_data='grand1')],
            [InlineKeyboardButton("حسینی & دای هون لی *2019", callback_data='grand2')],
            [InlineKeyboardButton("بازگشت", callback_data='back_to_categories')]
        ]
    elif category == 'didani':
        keyboard = [
            [InlineKeyboardButton("جام جهانی 2019", callback_data='didani1')],
            [InlineKeyboardButton("بیگی & کوک", callback_data='didani2')],
            [InlineKeyboardButton("ناک دان *جام جهانی 2019", callback_data='didani3')],
            [InlineKeyboardButton("بازگشت", callback_data='back_to_categories')]
        ]
    return InlineKeyboardMarkup(keyboard)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    return chat_member.status in [ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER]

async def handle_membership_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if await check_membership(update, context):
        keyboard = get_category_buttons()
        await query.message.delete()  # hazf payam
        await context.bot.send_message(chat_id=query.message.chat_id, text='دسته‌بندی ویدیوها را انتخاب کنید:', reply_markup=keyboard)
    else:
        await query.answer('لطفاً ابتدا در کانال عضو شوید.', show_alert=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await check_membership(update, context):
        keyboard = get_category_buttons()
        await update.message.reply_text('دسته‌بندی ویدیوها را انتخاب کنید:', reply_markup=keyboard)
    else:
        keyboard = get_join_channel_button()
        await update.message.reply_text('لطفاً ابتدا در کانال عضو شوید:', reply_markup=keyboard)

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    video_key = query.data
    video_url = VIDEO_URLS.get(video_key)
    if video_url:
        try:
            await query.message.delete()
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url)
        except Exception as e:
            logging.error(f'Error sending video: {e}')
            await query.message.reply_text('خطا در ارسال ویدیو.')
    else:
        await query.message.reply_text('ویدئو یافت نشد.')

async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    category = query.data.split('_')[1]
    keyboard = get_video_buttons(category)
    await query.message.edit_text(f'ویدیوهای بخش {category}:', reply_markup=keyboard)

async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = get_category_buttons()
    await query.message.edit_text('دسته‌بندی ویدیوها را انتخاب کنید:', reply_markup=keyboard)

def main() -> None:
    application = Application.builder().token(tk).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_membership_check, pattern='^check_membership$'))
    application.add_handler(CallbackQueryHandler(handle_category, pattern='^category_'))
    application.add_handler(CallbackQueryHandler(back_to_categories, pattern='^back_to_categories$'))
    application.add_handler(CallbackQueryHandler(send_video, pattern='^(olympic|world|grand|didani)[0-9]+$'))

    application.run_polling()

if __name__ == '__main__':
    main()
    