import os
from dotenv import load_dotenv
from services import Game
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN") # Безопасный токен из .env

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Хочешь поиграть в русский блекджек?")
    keyboard = [[InlineKeyboardButton("🎴 Играть в Блэкджек", callback_data="igrat")]]

    reply_markup = InlineKeyboardMarkup(keyboard) # разметка

    await update.message.reply_text(  # отправляем кнопку пользователю
        "Играть",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def logica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query # инфа о нажатии на кнопку
    await query.answer()

    game = context.user_data.get("game") # безопасно достанем ключ из хранилища данных одного пользователя
    
    # Если игры нет (пользователь нажал "Играть"), создаем новую
    if query.data == "igrat":
        game = Game()          # Создаем игру (сработает наш __init__)
        game.start()           # Раздаем карты
        context.user_data["game"] = game  # Сохраняем игру в память пользователя
        
        keyboard = [
            [InlineKeyboardButton("🃏 Взять", callback_data="vzyat")],
            [InlineKeyboardButton("✋ Пас", callback_data="pas")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Показываем карты игрока и ОДНУ карту дилера
        await query.edit_message_text(
            f"🃏 <b>Твои карты:</b> {' '.join(str(i3) for i3 in game.player_hand)} — <b>{game.calculate_score(game.player_hand)} очков</b>\n\n"
            f"🎴 <b>Карта дилера:</b> {game.dealer_hand[0]}\n\n"
            f"Взять ещё карту?",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    elif query.data == "vzyat":
        if not game:
            await query.edit_message_text("Нажми /start, чтобы начать новую игру!")
            return

        game.hit() # Игрок берет карту

        # Проверяем на перебор
        if game.calculate_score(game.player_hand) > 21:
            keyboard = [[InlineKeyboardButton("🔄 Играть снова", callback_data="igrat")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"🃏 <b>Твои карты:</b> {' '.join(str(c) for c in game.player_hand)} — <b>{game.calculate_score(game.player_hand)} очков</b>\n\n"
                f"💀 <b>Перебор!</b> Ты проиграл.",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        else:
            keyboard = [
                [InlineKeyboardButton("🃏 Взять", callback_data="vzyat")],
                [InlineKeyboardButton("✋ Пас", callback_data="pas")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"🃏 <b>Твои карты:</b> {' '.join(str(c) for c in game.player_hand)} — <b>{game.calculate_score(game.player_hand)} очков</b>\n\n"
                f"🎴 <b>Карта дилера:</b> {game.dealer_hand[0]}\n\n"
                f"Взять ещё карту?",
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    elif query.data == "pas":
        if not game:
            await query.edit_message_text("Нажми /start, чтобы начать новую игру!")
            return

        game.dealer_turn() # Дилер добирает карты
        result = game.winner() # Узнаем победителя

        keyboard = [[InlineKeyboardButton("🔄 Играть снова", callback_data="igrat")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🃏 <b>Твои карты:</b> {' '.join(str(c) for c in game.player_hand)} — <b>{game.calculate_score(game.player_hand)} очков</b>\n\n"
            f"🎴 <b>Карты дилера:</b> {' '.join(str(c) for c in game.dealer_hand)} — <b>{game.calculate_score(game.dealer_hand)} очков</b>\n\n"
            f"<b>{result}</b>",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(logica))
    app.run_polling()

if __name__ == "__main__":
    main()