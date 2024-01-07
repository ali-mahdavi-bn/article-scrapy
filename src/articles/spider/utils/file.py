import os

from articles.spider.utils.create_file_pdf import create_file_pdf, generate_file_name_with_url
from backbone.configs import config
from crawl.backbon.helpers.response import Response
from marker.convert_single import load_marker
from src.utils.minio_manager import minio_manager


def generate_file_text(response: Response):
    filename = generate_file_name_with_url(response=response)
    create_file_pdf(response=response, filename=filename)
    file_text = load_marker(filename)
    delete_file(filename)
    return file_text


def save_file_in_minio(response: Response):
    filename = generate_file_name_with_url(response=response)
    create_file_pdf(response=response, filename=filename)

    pdf_directory = config.PDF_WEB
    pdf_path = os.path.join(pdf_directory, filename + ".pdf")
    path_minio = minio_manager.upload_file("articles", filename, pdf_path)
    delete_file(filename)
    return path_minio


def delete_file(file: str) -> None:
    try:
        os.remove(config.PDF_WEB + f"{file}.pdf")
        print(f"The file '{file}' has been deleted successfully.")
    except:
        pass
