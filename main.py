#!/usr/bin/env python3
"""
Telegram Bot for English Language Learning
Designed for Railway deployment with runtime pip installation
"""

# Runtime dependency installation for Railway
import subprocess
import sys

def install_packages():
    """Install required packages at runtime"""
    packages = ['python-telegram-bot==20.7']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

try:
    import telegram
except ImportError:
    print("Installing dependencies...")
    install_packages()
    import telegram

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot configuration
BOT_TOKEN = "7552188554:AAHcBagKgJj2BkQQeFtaFMk_PQi_cBVPYqw"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Exercise data - Simple flat structure
EXERCISES = {
    "grammar_variations": {
        "title": "All grammar in one sentence",
        "description": "Master English grammar by seeing the same sentence in 52 different forms",
        "examples": [
            ("Present Simple", "She paints her house every summer. It's a tradition she follows to keep it vibrant."),
            ("Present Continuous", "Right now, she is painting her house with bright blue paint. I can see her from the street, brushing away."),
            ("Present Perfect", "She has just painted her house, and the fresh coat gleams in the sunlight."),
            ("Present Perfect Continuous", "She has been painting her house for two days straight, determined to finish before the weekend."),
            ("Past Simple", "Last summer, she painted her house in a bold red color. It stood out in the neighborhood."),
            ("Past Continuous", "When I visited her yesterday, she was painting her house, rollers and brushes scattered around her."),
            ("Past Perfect", "By the time the rain started, she had painted her house completely, avoiding any damage to her work."),
            ("Past Perfect Continuous", "She had been painting her house for hours when I arrived, and she was covered in specks of white paint."),
            ("Future Simple", "Next month, she will paint her house again, as she's planning a new color scheme."),
            ("Future Continuous", "Tomorrow afternoon, she will be painting her house, probably humming her favorite song."),
            ("Future Perfect", "By the end of next week, she will have painted her house, ready for the neighborhood party."),
            ("Future Perfect Continuous", "By the time the summer ends, she will have been painting her house on and off for three months, perfecting every detail."),
            ("Conditional (Present Real)", "If she has time this weekend, she paints her house to refresh its look."),
            ("Conditional (Present Unreal)", "If she had more free time, she would paint her house in a new shade every year."),
            ("Conditional (Past Unreal)", "If she had had a ladder last summer, she would have painted her house faster."),
            ("Conditional Perfect", "If the weather had been better, she would have painted her house by now."),
            ("Passive Voice (Present Simple)", "Her house is painted every summer, keeping it the envy of the street."),
            ("Passive Voice (Past Simple)", "Her house was painted last year, and it still looks stunning."),
            ("Passive Voice (Present Perfect)", "Her house has been painted recently, and the neighbors are already complimenting it."),
            ("Passive Voice (Future Simple)", "Her house will be painted next month by a professional team she hired."),
            ("Modal (Ability - Present)", "She can paint her house beautifully, thanks to her artistic skills."),
            ("Modal (Ability - Past)", "She could paint her house last summer without any help, impressing everyone."),
            ("Modal (Possibility - Present)", "She might paint her house this weekend if the weather stays clear."),
            ("Modal (Obligation - Present)", "She must paint her house soon because the old paint is peeling."),
            ("Modal (Advice - Present)", "She should paint her house before winter to protect it from the cold."),
            ("Modal (Intention - Future)", "She is going to paint her house next week, as she's already bought the supplies."),
            ("Subjunctive (Present)", "I suggest that she paint her house in a neutral color to appeal to future buyers."),
            ("Subjunctive (Past)", "I wished that she painted her house last month when the weather was perfect."),
            ("Imperative", "Paint your house this weekend, and I'll help you choose the colors!"),
            ("Gerund as Subject", "Painting her house is her favorite summer activity, bringing her joy every year."),
            ("Infinitive", "To paint her house is her goal for the summer, and she's excited to start."),
            ("Participle (Present)", "Painting her house, she feels a sense of accomplishment with every stroke."),
            ("Participle (Past)", "Having painted her house, she now relaxes on the porch, admiring her work."),
            ("Reported Speech (Past)", "She said that she painted her house last summer to surprise her family."),
            ("Reported Speech (Future)", "She told me that she would paint her house next month in a pastel shade."),
            ("Wish (Present)", "I wish she painted her house more often, as it always looks amazing."),
            ("Wish (Past)", "I wish she had painted her house last year, as the old color was fading."),
            ("Causative (Present)", "She has her house painted by professionals every few years to save time."),
            ("Causative (Past)", "She had her house painted last summer, and it transformed the entire look."),
            ("Negative (Present Simple)", "She doesn't paint her house often, preferring to hire someone instead."),
            ("Negative (Present Perfect)", "She hasn't painted her house yet this year, waiting for inspiration."),
            ("Question (Present Simple)", "Does she paint her house herself, or does she hire a team?"),
            ("Question (Present Perfect Continuous)", "Has she been painting her house all day, or did she take a break?"),
            ("Tag Question", "She paints her house every summer, doesn't she?"),
            ("Emphatic (Present)", "She does paint her house with such care, making it the best on the block."),
            ("Future in the Past", "I thought she would paint her house last weekend, but she postponed it."),
            ("Mixed Conditional", "If she had bought the paint earlier, she would be painting her house now."),
            ("Progressive Infinitive", "She loves to be painting her house, as it feels like a creative escape."),
            ("Perfect Infinitive", "She's happy to have painted her house before the neighborhood inspection."),
            ("Elliptical Construction", "She paints her house, and so do her neighbors, keeping the street colorful.")
        ]
    }
}

# Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when /start command is issued"""
    logger.info("Start command received")
    user = update.effective_user
    welcome_text = (
        f"👋 Welcome {user.first_name}!\n\n"
        "🎯 Master English Grammar Through Repetition\n\n"
        "This bot helps you learn English by showing the same sentence "
        "in different grammatical forms. By seeing familiar content in "
        "various contexts, you'll develop natural fluency.\n\n"
        "📚 Ready to start learning?"
    )
    
    keyboard = [[InlineKeyboardButton("🚀 Start Learning", callback_data="main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the main menu"""
    logger.info("Showing main menu")
    text = (
        "📚 Main Menu\n\n"
        "Choose an exercise type to begin:"
    )
    
    keyboard = [[InlineKeyboardButton("📝 All grammar in one sentence", callback_data="type_0")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_exercise_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display exercise description and start button"""
    logger.info("Showing exercise menu")
    query = update.callback_query
    await query.answer()
    
    exercise = EXERCISES["grammar_variations"]
    text = (
        f"📝 {exercise['title']}\n\n"
        f"{exercise['description']}\n\n"
        f"Total examples: {len(exercise['examples'])}\n\n"
        "Ready to begin?"
    )
    
    keyboard = [
        [InlineKeyboardButton("▶️ Start Exercise", callback_data="ex_0")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_example(update: Update, context: ContextTypes.DEFAULT_TYPE, index: int) -> None:
    """Display a specific example"""
    logger.info(f"Showing example {index}")
    query = update.callback_query
    await query.answer()
    
    exercise = EXERCISES["grammar_variations"]
    examples = exercise["examples"]
    
    if index >= len(examples):
        # Show congratulations screen
        text = (
            "🎉 Congratulations!\n\n"
            "You've completed all 52 grammar variations!\n\n"
            "Great job mastering different ways to express the same idea. "
            "Keep practicing to build natural fluency!"
        )
        keyboard = [
            [InlineKeyboardButton("🔄 Start Again", callback_data="ex_0")],
            [InlineKeyboardButton("📚 Exercise Menu", callback_data="type_0")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]
        ]
    else:
        # Show current example
        grammar_type, sentence = examples[index]
        progress = f"{index + 1}/{len(examples)}"
        
        text = (
            f"📖 Example {progress}\n\n"
            f"**{grammar_type}**\n\n"
            f"📝 {sentence}"
        )
        
        # Build navigation buttons
        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton("◀️ Back", callback_data=f"nav_{index - 1}"))
        
        if index < len(examples) - 1:
            nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"nav_{index + 1}"))
        else:
            nav_buttons.append(InlineKeyboardButton("Finish ✅", callback_data=f"nav_{index + 1}"))
        
        keyboard = [
            nav_buttons,
            [
                InlineKeyboardButton("📚 Exercise Menu", callback_data="type_0"),
                InlineKeyboardButton("🏠 Main Menu", callback_data="main")
            ]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks"""
    query = update.callback_query
    data = query.data
    
    logger.info(f"Callback data received: {data}")
    
    try:
        if data == "main":
            await show_main_menu(update, context)
        elif data == "type_0":
            await show_exercise_menu(update, context)
        elif data == "ex_0":
            await show_example(update, context, 0)
        elif data.startswith("nav_"):
            # Extract index from callback data
            index = int(data.split("_")[1])
            await show_example(update, context, index)
        else:
            logger.warning(f"Unknown callback data: {data}")
            await query.answer("Unknown action")
    except Exception as e:
        logger.error(f"Error in button_callback: {str(e)}")
        await query.answer("An error occurred. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(f'Update {update} caused error {context.error}')

async def post_init(application: Application) -> None:
    """Initialize the bot - delete any existing webhooks"""
    logger.info("Initializing bot...")
    await application.bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted (if any existed)")

def main() -> None:
    """Start the bot"""
    logger.info("Starting bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Check if we're running on Railway
    railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    
    if railway_domain:
        # Railway deployment - use webhook
        logger.info(f"Running on Railway with domain: {railway_domain}")
        port = int(os.environ.get("PORT", 8080))
        
        # Start webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"https://{railway_domain}/{BOT_TOKEN}",
            drop_pending_updates=True
        )
    else:
        # Local development - use polling
        logger.info("Running in polling mode (local development)")
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__':
    main()
