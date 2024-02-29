import os, sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Model.ElectronicReport import Electronic_report


async def main():
    Electronic_objects = await Electronic_report.objects.count()
    print(Electronic_objects)
    # for Electronic_obj in Electronic_objects:
    #     create_at = Electronic_obj.business_code
    #     print(create_at)


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
