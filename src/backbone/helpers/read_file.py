import io

import openpyxl
from fastapi import UploadFile


async def read_excel(file: UploadFile) -> openpyxl.Workbook:
    f = await file.read()
    xlsx = io.BytesIO(f)
    return openpyxl.load_workbook(xlsx)
