import os
from typing import Any, Dict
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


async def send_to_user(data: Dict[str, Any]):
    """Send message to user through bot"""

    try:
        user_id = os.getenv("TELEGRAM_USER_ID")
        # print(user_id)
        # user_id = data.get("user_id")
        message = data.get("message")

        if not message:
            raise HTTPException(
                status_code=400, detail="Missing required message to send"
            )
        elif not user_id.isdigit():
            raise HTTPException(status_code=400, detail="Invalid/unavailable user ID")

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
