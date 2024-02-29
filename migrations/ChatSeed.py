import orm
import os, sys ,pytz
from datetime import datetime
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Model.Chat import ChatModel 
from migrations.create_table import convert_to_vietnam_time

async def main():
    # user = await User.objects.create( name="John Doe", username="john_doe")

    # # # Seed Chat data
    # await Chat.objects.create( user_id=user, message="Hello, World 3!")
    chat_objects  = await ChatModel.objects.all()
    for chat_obj in chat_objects :
        create_at = chat_obj.create_at
        vietnam_time = convert_to_vietnam_time(create_at)
        print(vietnam_time)

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
