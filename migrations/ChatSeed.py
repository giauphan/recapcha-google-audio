import os, sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from Model.ElectronicReport import Electronic_report


async def main():
    count = await Electronic_report.objects.count()
    print(count)

import asyncio

if __name__ == "__main__":
    asyncio.run(main())
