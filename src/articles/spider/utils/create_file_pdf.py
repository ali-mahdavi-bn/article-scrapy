import os
from datetime import datetime


from backbone.configs import config
from crawl.backbon.helpers.response import Response


def create_file_pdf(response: Response, filename: str) -> str:
    pdf_directory = config.PDF_WEB
    pdf_path = os.path.join(pdf_directory, filename + ".pdf")

    # Check if the directory exists, create if not
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # Create and write to the file
    with open(pdf_path, "wb") as f:
        binary_representation = ''.join(format(ord(char), '08b') for char in response.body)

        # Encode the string as bytes before writing to the file
        f.write(binary_representation.encode('utf-8'))
    return "filename"


def generate_file_name_with_url(response: Response) -> str:
    return ((response.url.split("/")[-1]).strip())[:-4]
