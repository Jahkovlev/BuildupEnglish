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
# Simplified structure - just the examples
EXERCISE_EXAMPLES = [
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

# ==================== BOT HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the main menu when the command /start is issued."""
    keyboard = [[InlineKeyboardButton("📚 All grammar in one sentence", callback_data="menu_grammar")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to the English Learning Bot! 🎓\n\n"
        "Choose an exercise type to start learning:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    data = query.data
    
    # Log for debugging
    logger.info(f"Callback data received: {data}")
    
    await query.answer()
    
    if data == "main":
        # Show main menu
        keyboard = [[InlineKeyboardButton("📚 All grammar in one sentence", callback_data="menu_grammar")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Choose an exercise type to start learning:",
            reply_markup=reply_markup
        )
    
    elif data == "menu_grammar":
        # Show exercise list
        keyboard = [[InlineKeyboardButton("She paints her house", callback_data="start_0")]]
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Choose an exercise from 'All grammar in one sentence':",
            reply_markup=reply_markup
        )
    
    elif data.startswith("start_"):
        # Start exercise at index 0
        await show_example(query, 0)
    
    elif data.startswith("ex_"):
        # Navigate to specific example
        try:
            index = int(data.split("_")[1])
            await show_example(query, index)
        except (ValueError, IndexError):
            await query.edit_message_text("Error: Invalid navigation.")

async def show_example(query, index: int) -> None:
    """Show a specific example."""
    examples = EXERCISE_EXAMPLES
    
    # Check if this is the last example
    if index >= len(examples):
        await query.edit_message_text(
            f"🎉 **CONGRATULATIONS!** 🎉\n\n"
            f"You've completed all {len(examples)} examples!\n\n"
            f"Great work! You've seen how this sentence works in all different grammar forms. "
            f"Keep practicing to master your English fluency! 💪",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 All grammar in one sentence", callback_data="menu_grammar")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main")]
            ])
        )
        return
    
    # Show current example
    grammar_type, sentence = examples[index]
    
    # Build navigation keyboard
    keyboard = []
    nav_row = []
    
    # Back button (only if not at the beginning)
    if index > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"ex_{index-1}"))
    
    # Next/Finish button
    if index < len(examples) - 1:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"ex_{index+1}"))
    else:
        nav_row.append(InlineKeyboardButton("Finish ✅", callback_data=f"ex_{index+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Add menu buttons
    keyboard.append([InlineKeyboardButton("📚 All grammar in one sentence", callback_data="menu_grammar")])
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Format the message
    message = (
        f"**She paints her house** ({index + 1}/{len(examples)})\n\n"
        f"**{grammar_type}:**\n"
        f"_{sentence}_"
    )
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

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
