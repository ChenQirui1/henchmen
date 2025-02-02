from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging
from typing import Dict, Any

from dotenv import load_dotenv
import os


from messager import send_to_user

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SERVER_URL = "http://localhost:8000"

# Initialize bot and dispatcher
session = AiohttpSession()
bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()
router = Router()

# FastAPI app
app = FastAPI()


class ServerRequest(BaseModel):
    user_id: int
    text: str
    data: Dict[str, Any] = {}


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command"""
    await message.answer("Bot is running! Use /help to see available commands.")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/status - Check server connection
/senddata - Send data to server
    """
    await message.answer(help_text)


@router.message(Command("status"))
async def cmd_status(message: Message):
    """Check server connection status"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{SERVER_URL}/health") as response:
                if response.status == 200:
                    await message.answer("Server is connected and healthy!")
                else:
                    await message.answer("Server is not responding properly.")
    except Exception as e:
        await message.answer(f"Failed to connect to server: {str(e)}")


@router.message(Command("senddata"))
async def cmd_send_data(message: Message):
    """Send data to server"""
    try:
        data = {
            "user_id": message.from_user.id,
            "text": message.text,
            "data": {
                "username": message.from_user.username,
                "chat_id": message.chat.id,
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{SERVER_URL}/process-data", json=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    await message.answer(f"Server response: {result['message']}")
                else:
                    await message.answer("Failed to process data on server.")
    except Exception as e:
        await message.answer(f"Error sending data: {str(e)}")


# Server endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/process-data")
async def process_data(request: ServerRequest):
    """Process data received from bot"""
    try:
        # Process the received data
        logger.info(f"Processing data for user {request.user_id}")

        # Example processing - you can modify this based on your needs
        processed_result = {
            "message": f"Processed data from user {request.user_id}",
            "received_text": request.text,
            "extra_data": request.data,
        }

        return processed_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/send-to-user")
# async def send_to_user(data: Dict[str, Any]):
#     """Send message to user through bot"""
#     try:
#         await send_to_user(data)
#         return {"status": "success"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/t")
async def update_task(data: Dict[str, Any]):

    try:
        # user_id = data.get("user_id")
        message = data.get("message")

        # update the agent with the new message

        # send the message to the user through the bot message.answer

        await send_to_user({"message": message})
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/r")
async def remind_user(data: Dict[str, Any]):
    """Remind user with a message"""

    user_id = os.getenv("TELEGRAM_USER_ID")

    await bot.send_message(user_id, "Not implemented yet :(")

    return {"status": "success"}


@app.post("/i")
async def record_knowledge(data: Dict[str, Any]):

    user_id = os.getenv("TELEGRAM_USER_ID")

    await bot.send_message(user_id, "Not implemented yet :(")

    return {"status": "success"}


async def main():
    """Main function to run bot and server"""
    # Register routers
    dp.include_router(router)

    # Start bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Run the server in a separate process
    import multiprocessing

    server_process = multiprocessing.Process(
        target=uvicorn.run, args=(app,), kwargs={"host": "0.0.0.0", "port": 8000}
    )
    server_process.start()

    # Run the bot
    asyncio.run(main())
