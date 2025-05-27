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
        "Welcome to the English Learning Bot! 🎓\n\n"
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
    
    print(f"show_exercise called - type: '{exercise_type}', key: '{exercise_key}', idx: {example_idx}")
    print(f"Available exercises: {list(EXERCISES.keys())}")
    logger.info(f"show_exercise called - type: {exercise_type}, key: {exercise_key}, idx: {example_idx}")
    logger.info(f"Available exercises: {list(EXERCISES.keys())}")
    
    if exercise_type in EXERCISES:
        print(f"Exercise keys for {exercise_type}: {list(EXERCISES[exercise_type]['exercises'].keys())}")
        logger.info(f"Exercise keys for {exercise_type}: {list(EXERCISES[exercise_type]['exercises'].keys())}")
    
    if exercise_type not in EXERCISES or exercise_key not in EXERCISES[exercise_type]["exercises"]:
        print(f"Exercise not found! Type '{exercise_type}' in EXERCISES: {exercise_type in EXERCISES}")
        if exercise_type in EXERCISES:
            print(f"Key '{exercise_key}' in exercises: {exercise_key in EXERCISES[exercise_type]['exercises']}")
        await query.edit_message_text("Exercise not found.")
        return
    
    exercise = EXERCISES[exercise_type]["exercises"][exercise_key]
    examples = exercise["examples"]
    
    if example_idx < 0 or example_idx >= len(examples):
        example_idx = 0
    
    # Check if user clicked "Next" on the last example
    if example_idx >= len(examples):
        # User has completed the exercise!
        await query.edit_message_text(
            f"🎉 **CONGRATULATIONS!** 🎉\n\n"
            f"You've completed all {len(examples)} examples of '{exercise['title']}'!\n\n"
            f"Great work! You've seen how this sentence works in all different grammar forms. "
            f"Keep practicing to master your English fluency! 💪",
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
    
    # Next button - check if it's the last example
    if example_idx < len(examples) - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"nav_{exercise_type}_{exercise_key}_{example_idx+1}"))
    else:
        # Last example - clicking next will show congratulations
        nav_row.append(InlineKeyboardButton("Finish ✅", callback_data=f"nav_{exercise_type}_{exercise_key}_{example_idx+1}"))
    
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
    
    # Debug logging
    print(f"Button callback received: {data}")
    logger.info(f"Button callback received: {data}")
    
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
        print(f"Exercise callback parts: {data.split('_')}")
        logger.info(f"Exercise callback parts: {data.split('_')}")
        parts = data.split("_", 2)
        if len(parts) == 3:
            exercise_type = parts[1]
            exercise_key = parts[2]
            print(f"Starting exercise - type: {exercise_type}, key: {exercise_key}")
            logger.info(f"Starting exercise - type: {exercise_type}, key: {exercise_key}")
            await show_exercise(update, context, exercise_type, exercise_key, 0)
        else:
            # Handle old format (shouldn't happen with current code)
            print(f"Invalid format - parts: {parts}")
            await query.answer("Invalid exercise format. Please go back to main menu.")
            await query.edit_message_text("Invalid exercise format. Please go back to main menu.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]]))
    
    elif data.startswith("nav_"):
        # Navigate within an exercise
        parts = data.split("_")
        if len(parts) >= 4:
            exercise_type = parts[1]
            exercise_key = parts[2]
            # Join remaining parts in case exercise_key had underscores
            if len(parts) > 4:
                exercise_key = "_".join(parts[2:-1])
                example_idx = int(parts[-1])
            else:
                example_idx = int(parts[3])
            await show_exercise(update, context, exercise_type, exercise_key, example_idx)
        else:
            await query.answer("Navigation error. Please try again.")

def main() -> None:
    """Start the bot."""
    # Get token from environment variable
    TOKEN = os.environ.get("BOT_TOKEN")
    
    if not TOKEN:
        print("ERROR: BOT_TOKEN environment variable not set!")
        print("Please set BOT_TOKEN in your Railway environment variables.")
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
