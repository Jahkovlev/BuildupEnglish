import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Exercise data - Add new exercises here only
EXERCISES = {
    "she_paints_house": {
        "title": "She paints her house",
        "examples": [
            ("Present Simple", "She paints her house every summer."),
            ("Present Continuous", "She is painting her house right now."),
            ("Present Perfect", "She has just painted her house."),
            ("Past Simple", "She painted her house last summer."),
            ("Future Simple", "She will paint her house next month."),
            # Add more examples as needed
        ]
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message when /start is issued."""
    keyboard = [[InlineKeyboardButton("📚 Start Exercise", callback_data="start_exercise")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Welcome to BuildUpEnglish Bot! 🎓\n\nLet's learn English grammar!",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "start_exercise":
        # Start the exercise
        context.user_data['current_index'] = 0
        await show_example(query, context)
    
    elif query.data.startswith("nav_"):
        # Navigation
        direction = query.data.split("_")[1]
        current = context.user_data.get('current_index', 0)
        
        if direction == "next":
            context.user_data['current_index'] = current + 1
        else:  # back
            context.user_data['current_index'] = max(0, current - 1)
        
        await show_example(query, context)
    
    elif query.data == "main_menu":
        # Back to start
        keyboard = [[InlineKeyboardButton("📚 Start Exercise", callback_data="start_exercise")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Welcome back! Ready to practice more?",
            reply_markup=reply_markup
        )

async def show_example(query, context: ContextTypes.DEFAULT_TYPE):
    """Show current example."""
    examples = EXERCISES["she_paints_house"]["examples"]
    current_idx = context.user_data.get('current_index', 0)
    
    if current_idx >= len(examples):
        # Completed!
        await query.edit_message_text(
            "🎉 Congratulations! You've completed all examples!\n\nGreat work!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
            ]])
        )
        return
    
    # Show current example
    grammar_type, sentence = examples[current_idx]
    
    keyboard = []
    nav_buttons = []
    
    if current_idx > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Back", callback_data="nav_back"))
    nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data="nav_next"))
    
    keyboard.append(nav_buttons)
    keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")])
    
    await query.edit_message_text(
        f"**Example {current_idx + 1}/{len(examples)}**\n\n"
        f"**{grammar_type}:**\n{sentence}",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    """Start the bot."""
    # Get token from environment variable or use hardcoded (not recommended for production)
    TOKEN = os.environ.get("BOT_TOKEN", "7552188554:AAFMQ8DbThjqkmYbJ35eneAW6-QKiqjyuO0")
    
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
