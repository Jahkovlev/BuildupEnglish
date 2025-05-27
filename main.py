import subprocess
import sys
import os

# Force install dependencies at runtime
try:
    import telegram
except ImportError:
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
    print("Dependencies installed!")

# Now import normally
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Simple exercise data
EXERCISES = {
    "she_paints_house": [
        ("Present Simple", "She paints her house every summer."),
        ("Present Continuous", "She is painting her house right now."),
        ("Present Perfect", "She has just painted her house."),
        ("Past Simple", "She painted her house last summer."),
        ("Future Simple", "She will paint her house next month."),
    ]
}

# Current exercise state (simple approach)
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the main menu when the command /start is issued."""
    user_id = update.effective_user.id
    user_states[user_id] = {"exercise": "she_paints_house", "index": 0}
    
    keyboard = [[InlineKeyboardButton("📚 Start Exercise: She paints her house", callback_data="start_exercise")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to BuildUpEnglish Bot! 🎓\n\n"
        "Let's learn English grammar through examples!",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    if data == "start_exercise":
        # Reset to first example
        user_states[user_id] = {"exercise": "she_paints_house", "index": 0}
        await show_example(query, user_id)
    
    elif data == "next":
        # Move to next example
        if user_id in user_states:
            user_states[user_id]["index"] += 1
            await show_example(query, user_id)
    
    elif data == "back":
        # Move to previous example
        if user_id in user_states and user_states[user_id]["index"] > 0:
            user_states[user_id]["index"] -= 1
            await show_example(query, user_id)
    
    elif data == "main_menu":
        # Show main menu
        keyboard = [[InlineKeyboardButton("📚 Start Exercise: She paints her house", callback_data="start_exercise")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Welcome back! Ready to practice more?",
            reply_markup=reply_markup
        )

async def show_example(query, user_id: int) -> None:
    """Show the current example."""
    if user_id not in user_states:
        await query.edit_message_text("Please start over with /start")
        return
    
    state = user_states[user_id]
    examples = EXERCISES[state["exercise"]]
    index = state["index"]
    
    # Check if finished
    if index >= len(examples):
        await query.edit_message_text(
            "🎉 **CONGRATULATIONS!** 🎉\n\n"
            "You've completed all examples!\n\n"
            "Great work! You've seen how this sentence works in different grammar forms.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
            ]])
        )
        return
    
    # Show current example
    grammar_type, sentence = examples[index]
    
    # Build navigation
    keyboard = []
    nav_row = []
    
    if index > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Back", callback_data="back"))
    
    if index < len(examples) - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data="next"))
    else:
        nav_row.append(InlineKeyboardButton("Finish ✅", callback_data="next"))
    
    keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
    
    message = (
        f"**Example {index + 1}/{len(examples)}**\n\n"
        f"**{grammar_type}:**\n"
        f"{sentence}"
    )
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main() -> None:
    """Start the bot."""
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("ERROR: BOT_TOKEN environment variable not set!")
        sys.exit(1)
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
