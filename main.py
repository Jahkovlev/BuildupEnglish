import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Exercise data
EXERCISES = {
    "all_grammar_one_sentence": {
        "name": "All grammar in one sentence",
        "exercises": {
            "she_paints_house": {
                "title": "She paints her house",
                "examples": [
                    ("Present Simple", "She paints her house every summer."),
                    ("Present Continuous", "She is painting her house right now."),
                    ("Present Perfect", "She has just painted her house."),
                    ("Past Simple", "She painted her house last summer."),
                    ("Future Simple", "She will paint her house next month."),
                ]
            }
        }
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the main menu when the command /start is issued."""
    keyboard = []
    
    for ex_type_key, ex_type_data in EXERCISES.items():
        keyboard.append([InlineKeyboardButton(ex_type_data["name"], callback_data=f"type_{ex_type_key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to BuildUpEnglish Bot! 🎓\n\nChoose an exercise type:",
        reply_markup=reply_markup
    )

async def show_exercise_list(update: Update, context: ContextTypes.DEFAULT_TYPE, exercise_type: str) -> None:
    """Show list of exercises for a specific type."""
    query = update.callback_query
    await query.answer()
    
    keyboard = []
    exercises = EXERCISES[exercise_type]["exercises"]
    
    for ex_key, ex_data in exercises.items():
        keyboard.append([InlineKeyboardButton(ex_data["title"], callback_data=f"ex_{exercise_type}_{ex_key}")])
    
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"Choose an exercise from '{EXERCISES[exercise_type]['name']}':",
        reply_markup=reply_markup
    )

async def show_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE, exercise_type: str, exercise_key: str, example_idx: int = 0) -> None:
    """Show a specific exercise example."""
    query = update.callback_query
    await query.answer()
    
    exercise = EXERCISES[exercise_type]["exercises"][exercise_key]
    examples = exercise["examples"]
    
    if example_idx >= len(examples) - 1:
        await query.edit_message_text(
            f"🎉 **CONGRATULATIONS!** 🎉\n\nYou've completed all examples!",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
            ])
        )
        return
    
    grammar_type, sentence = examples[example_idx]
    
    keyboard = []
    nav_row = []
    
    if example_idx > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"nav_{exercise_type}_{exercise_key}_{example_idx-1}"))
    
    nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"nav_{exercise_type}_{exercise_key}_{example_idx+1}"))
    keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = (
        f"**Example {example_idx + 1}/{len(examples)}**\n\n"
        f"**{grammar_type}:**\n{sentence}"
    )
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    data = query.data
    
    if data == "main_menu":
        keyboard = []
        for ex_type_key, ex_type_data in EXERCISES.items():
            keyboard.append([InlineKeyboardButton(ex_type_data["name"], callback_data=f"type_{ex_type_key}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.answer()
        await query.edit_message_text(
            "Choose an exercise type:",
            reply_markup=reply_markup
        )
    
    elif data.startswith("type_"):
        exercise_type = data.replace("type_", "")
        await show_exercise_list(update, context, exercise_type)
    
    elif data.startswith("ex_"):
        parts = data.split("_", 2)
        exercise_type = parts[1]
        exercise_key = parts[2]
        await show_exercise(update, context, exercise_type, exercise_key, 0)
    
    elif data.startswith("nav_"):
        parts = data.split("_")
        exercise_type = parts[1]
        exercise_key = parts[2]
        example_idx = int(parts[3])
        await show_exercise(update, context, exercise_type, exercise_key, example_idx)

def main() -> None:
    """Start the bot."""
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("ERROR: BOT_TOKEN environment variable not set!")
        import sys
        sys.exit(1)
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
