import os, sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Model.ElectronicReport import Electronic_report


async def main():
    count = await Electronic_report.objects.count()
    if count > 0:
        Electronic_objects = await Electronic_report.objects.filter(status=True).all()

        for Electronic_obj in Electronic_objects:
            create_at = Electronic_obj.id
            await Electronic_report.objects.filter(
                business_code=Electronic_obj.business_code
            ).update(status=False)

            print(create_at)


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
