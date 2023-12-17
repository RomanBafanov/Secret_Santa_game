from secret_santa.bot_logic.loader import dp, bot
from secret_santa.bot_logic.set_bot_commands import set_commands
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from secret_santa.bot_logic.statesform import StepsForm
from aiogram import types, F


NAME = None
PLAYER_E_MAIL = None
PLAYER_INTERESTS = None
PLAYER_LETTER = None


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await set_commands(bot)
    text = message.text.split()
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEK9qFlevsInA68q_W-0N39iF5-5CCrjwACeAEAAiI3jgQ6pl0vZ69f1TME')
    if len(text) > 1:
        id_organizer = text[1]
        # Запрос на информацию об игре
        await message.answer(f"Замечательно, ты собираешься участвовать в игре: {id_organizer}")
                             # "(вывести на экран данные об игре: название, ограничение стоимости подарка, "
                             # "период регистрации и дата отправки подарков)")
        await message.answer("Для участия пройди регистрацию.\n"
                             "Напиши своё имя")
        await state.set_state(StepsForm.PLAYER_NAME)
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Создать игру", callback_data="Создать игру")
        )
        await message.answer("Организуй тайный обмен подарками, 🎄🎄🎄\n"
                             "🎄🎄🎄 запусти праздничное настроение!",
                             reply_markup=builder.as_markup())
    # referral_link = f"https://t.me/Secret_Santa_educational_bot?start={id_user}"
    # print(referral_link)
    # await message.answer("Организуй тайный обмен подарками, запусти праздничное настроение!")


@dp.message(StepsForm.PLAYER_NAME)
async def new_player(message: types.Message, state: FSMContext):
    await state.clear()
    global NAME
    NAME = message.text
    await message.answer(f"Замечательно {NAME}! Теперь введи адрес электронной почты")
    await state.set_state(StepsForm.E_MAIL)


@dp.message(StepsForm.E_MAIL)
async def player_email(message: types.Message, state: FSMContext):
    await state.clear()
    global PLAYER_E_MAIL
    PLAYER_E_MAIL = message.text
    await message.answer("Отлично! Теперь напиши о своих увлечениях, интересах, "
                         "чтобы Тайный Санта знал чего ты хочешь. Не более 75 символов")
    await state.set_state(StepsForm.INTERESTS)


@dp.message(StepsForm.INTERESTS)
async def player_interests(message: types.Message, state: FSMContext):
    await state.clear()
    global PLAYER_INTERESTS
    PLAYER_INTERESTS = message.text
    if len(PLAYER_INTERESTS) > 75:
        difference = len(PLAYER_INTERESTS) - 75
        await message.answer(f"Нужно ввести не более 75 символов. Введи текст короче на {difference}")
        await state.set_state(StepsForm.INTERESTS)
    else:
        builder = InlineKeyboardBuilder()
        builder.row(types.InlineKeyboardButton(
            text="Пропустить", callback_data="Пропустить письмо")
        )
        await message.answer("Теперь Санте будет проще найти тебе подарок! "
                             "Теперь ты можешь написать Санте письмо! Не более 200 символов",
                             reply_markup=builder.as_markup())
        await state.set_state(StepsForm.LETTER)


@dp.message(StepsForm.LETTER)
async def player_letter(message: types.Message, state: FSMContext):
    await state.clear()
    global PLAYER_LETTER
    PLAYER_LETTER = message.text
    if len(PLAYER_LETTER) > 200:
        difference = len(PLAYER_LETTER) - 200
        await message.answer(f"Нужно ввести не более 200 символов. Введи текст короче на {difference}")
        await state.set_state(StepsForm.LETTER)
    else:
        await message.answer("Превосходно, ты в игре! "
                             "\"Дата\" мы проведем жеребьевку и ты узнаешь имя и контакты своего тайного друга. "
                             "Ему и нужно будет подарить подарок!")


@dp.callback_query(F.data == "Пропустить письмо")
async def player_letter(callback: types.CallbackQuery, state: FSMContext):
    global PLAYER_LETTER
    PLAYER_LETTER = callback.message.text
    if len(PLAYER_LETTER) > 200:
        difference = len(PLAYER_LETTER) - 200
        await callback.message.answer(f"Нужно ввести не более 200 символов. Введи текст короче на {difference}")
        await state.set_state(StepsForm.LETTER)
    else:
        await callback.message.answer("Превосходно, ты в игре! "
                                      "\"Дата\" мы проведем жеребьевку и ты узнаешь имя "
                                      "и контакты своего тайного друга. "
                                      "Ему и нужно будет подарить подарок!")
