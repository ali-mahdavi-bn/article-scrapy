import os
from datetime import datetime


from backbone.configs import config
from crawl.helper.helpers.response import Response


def create_file_pdf(response: Response, filename: str) -> str:
    pdf_directory = config.PDF_WEB
    pdf_path = os.path.join(pdf_directory, filename + ".pdf")

    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    with open(pdf_path, "wb") as f:
        f.write(response.content)
    return filename


def generate_file_name_with_url(response: Response) -> str:
    return ((response.url.split("/")[-1]).strip())[:-4]
