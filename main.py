from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from token_for_bot import bot_token
from resourses.Local_msg import Local
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def start_handler(message:types.Message):
    await message.reply(Local.welcome)


@dp.message_handler(commands=["help"])
async def help_handler(message:types.Message):
    await message.reply(Local.help)

class StepsForm(StatesGroup):
    get_name = State()
    get_last_name = State()
    get_age = State()



@dp.message_handler(commands=["register"])
async def register_handler(message:types.Message, state: FSMContext):
    await message.answer("Start to register. Input your name:")
    await state.set_state(StepsForm.get_name)

@dp.message_handler(content_types=types.ContentType.TEXT , state=StepsForm.get_name)
async def get_name(message:types.Message, state: FSMContext):
    await message.answer(f"Your name is {message.text}, input your last name:")
    await state.update_data(name = message.text)
    await state.set_state(StepsForm.get_last_name)

@dp.message_handler(content_types=types.ContentType.TEXT, state=StepsForm.get_last_name)
async def get_last_name(message:types.Message, state: FSMContext):
    await message.answer(f"Your last name is {message.text}, input your age")
    await state.update_data(last_name = message.text)
    await state.set_state(StepsForm.get_age)

@dp.message_handler(content_types=types.ContentType.TEXT, state=StepsForm.get_age)
async def get_age(message:types.Message, state: FSMContext):
    await message.answer(f"Your age is {message.text}")
    await state.update_data(age = int(message.text))
    saved_data = await state.get_data()
    name = saved_data["name"]
    last_name = saved_data["last_name"]
    age = saved_data["age"]
    await message.answer(f"Your full name is {name} {last_name} and your age is {age}")
    await state.reset_data()
    cleared_data = await state.get_data()
    await message.answer(cleared_data)


executor.start_polling(dp)