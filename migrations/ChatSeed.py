import os, sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Model.ElectronicReport import Electronic_report


async def main():
    Electronic_objects = await Electronic_report.objects.all()
    business_code = 12322
    check_business_code = await Electronic_report.objects.filter(
        business_code=business_code
    ).exists()
    if check_business_code == False:
        await Electronic_report.objects.create(
            business_name="null",
            business_code=business_code,
            location="null",
            registration_period=datetime.utcnow(),
        )
    for Electronic_obj in Electronic_objects:
        create_at = Electronic_obj.business_name
        print(create_at)


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
