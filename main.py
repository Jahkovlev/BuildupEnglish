import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

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
    keyboard = [[InlineKeyboardButton("📚 Start Learning", callback_data="type_all_grammar_one_sentence")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to BuildUpEnglish Bot! 🎓", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "type_all_grammar_one_sentence":
        keyboard = [[InlineKeyboardButton("She paints her house", callback_data="ex_0")]]
        keyboard.append([InlineKeyboardButton("🏠 Main Menu", callback_data="main")])
        await query.edit_message_text("Choose an exercise:", reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("ex_"):
        idx = int(data.split("_")[1])
        examples = EXERCISES["all_grammar_one_sentence"]["exercises"]["she_paints_house"]["examples"]
        
        if idx >= len(examples):
            await query.edit_message_text("🎉 Congratulations! You completed all examples!")
            return
        
        grammar, sentence = examples[idx]
        keyboard = []
        
        if idx > 0:
            keyboard.append([
                InlineKeyboardButton("⬅️ Back", callback_data=f"ex_{idx-1}"),
                InlineKeyboardButton("Next ➡️", callback_data=f"ex_{idx+1}")
            ])
        else:
            keyboard.append([InlineKeyboardButton("Next ➡️", callback_data=f"ex_{idx+1}")])
        
        keyboard.append([InlineKeyboardButton("🏠 Main Menu
