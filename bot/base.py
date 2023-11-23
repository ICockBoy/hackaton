from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.config import token
from bot.database.all import All

scheduler = AsyncIOScheduler()
dbase = All()
memory_storage = MemoryStorage()
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(storage=memory_storage)
