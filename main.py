import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== EXERCISE POOL ====================
# IMPORTANT: Only add exercises to this pool. Do not modify exercises elsewhere in the code.

EXERCISES = {
    "all_grammar_one_sentence": {
        "name": "All grammar in one sentence",
        "exercises": {
            "she_paints_house": {
                "title": "She paints her house",
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
                    # Add more examples as needed
                ]
            }
        }
    }
}

# ==================== BOT HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the main menu when the command /start is issued."""
    keyboard = []
    
    # Add exercise types
    for ex_type_key, ex_type_data in EXERCISES.items():
        keyboard.append([InlineKeyboardButton(ex_type_data["name"], callback_data=f"type_{ex_type_key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to BuildUpEnglish Bot! 🎓\n\n"
        "Choose an exercise type to start learning:",
        reply_markup=reply_markup
    )

async def show_exercise_list(update: Update, context: ContextTypes.DEFAULT_TYPE, exercise_type: str) -> None:
    """Show list of exercises for a specific type."""
    query = update.callback_query
    await query.answer()
    
    if exercise_type not in EXERCISES:
        await query.edit_message_text("Exercise type not found.")
        return
    
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
    
    if exercise_type not in EXERCISES or exercise_key not in EXERCISES[exercise_type]["exercises"]:
        await query.edit_message_text("Exercise not found.")
        return
    
    exercise = EXERCISES[exercise_type]["exercises"][exercise_key]
    examples = exercise["examples"]
    
    if example_idx < 0 or example_idx >= len(examples):
        example_idx = 0
    
    # Check if this is the last example
    if example_idx == len(examples) - 1:
        # User has completed the exercise!
        await query.edit_message_text(
            f"🎉 **CONGRATULATIONS!** 🎉\n\n"
            f"You've completed all {len(examples)} examples of '{exercise['title']}'!\n\n"
            f"Great work! Keep practicing to master your English fluency! 💪",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 " + EXERCISES[exercise_type]["name"], callback_data=f"type_{exercise_type}")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
            ])
        )
        return
    
    # Show current example
    grammar_type, sentence = examples[example_idx]
    
    # Build navigation keyboard
    keyboard = []
    nav_row = []
    
    # Back button (only if not at the beginning)
    if example_idx > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"nav_{exercise_type}_{exercise_key}_{example_idx-1}"))
    
    # Next button
    nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"nav_{exercise_type}_{exercise_key}_{example_idx+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Add exercise type and main menu buttons
    keyboard.append([InlineKeyboardButton("📚 " + EXERCISES[exercise_type]["name"], callback_data=f"type_{exercise_type}")])
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Format the message
    message = (
        f"**{exercise['title']}** ({example_idx + 1}/{len(examples)})\n\n"
        f"**{grammar_type}:**\n"
        f"_{sentence}_"
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
        # Show main menu
        keyboard = []
        for ex_type_key, ex_type_data in EXERCISES.items():
            keyboard.append([InlineKeyboardButton(ex_type_data["name"], callback_data=f"type_{ex_type_key}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.answer()
        await query.edit_message_text(
            "Choose an exercise type to start learning:",
            reply_markup=reply_markup
        )
    
    elif data.startswith("type_"):
        # Show exercises for this type
        exercise_type = data.replace("type_", "")
        await show_exercise_list(update, context, exercise_type)
    
    elif data.startswith("ex_"):
        # Start an exercise
        parts = data.split("_", 2)
        exercise_type = parts[1]
        exercise_key = parts[2]
        await show_exercise(update, context, exercise_type, exercise_key, 0)
    
    elif data.startswith("nav_"):
        # Navigate within an exercise
        parts = data.split("_")
        exercise_type = parts[1]
        exercise_key = parts[2]
        example_idx = int(parts[3])
        await show_exercise(update, context, exercise_type, exercise_key, example_idx)

def main() -> None:
    """Start the bot."""
    # Get token from environment variable
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("ERROR: BOT_TOKEN environment variable not set!")
        print("Please set BOT_TOKEN in your Railway environment variables.")
        import sys
        sys.exit(1)
    
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Run the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
