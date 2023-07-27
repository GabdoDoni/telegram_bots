from aiogram import Router
from aiogram.types import Message
from market.lexicon.lexicon_ru import LEXICON
from market.keyboards.keyboard_utils import db_add_product, list_product_keyboard, delete_product_keyboard, start_keyboard

router: Router = Router()


# Этот хэндлер будет срабатывать на остальные любые сообщения
@router.message()
async def other_text_answers(message: Message):
    await message.answer(LEXICON['no_no'], reply_markup=start_keyboard)