from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from telethon import TelegramClient, events, types

from __future__ import annotations  # Import annotations feature from Python 3.7

api_id = 21827985
api_hash = '249159e0fc539bb9bce0d5e974c44f88'

phone = '+601156292264'
session_file = 'xzy0207'
password = '0207'

response_message = "1"  # Updated auto-reply message
group_chat_ids = [-1001766161750, -1001863685543]
sender_ids = [1814850031, 6070986947, 1518090731, 5042719163]

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    client = TelegramClient(session_file, api_id, api_hash)
    await client.start(phone)

    @client.on(events.NewMessage())
    async def auto_reply(event):
        if (
            event.media
            and isinstance(event.media, types.MessageMediaPhoto)
            and event.chat_id in group_chat_ids
            and event.sender_id in sender_ids
        ):
            sender = await event.get_sender()

            # Respond with the updated message "1"
            await event.respond(response_message)

    await client.run_until_disconnected()

@app.get("/")
async def root():
    return {"message": "Telegram auto-reply service is running!"}

if __name__ == '__main__':
    import uvicorn
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    uvicorn.run(app, host="0.0.0.0", port=8000)
