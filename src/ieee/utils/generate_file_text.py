from scrapy.http import HtmlResponse

from ieee.utils.create_file_pdf import create_file_pdf, generate_file_name_with_url
from ieee.utils.remove_file import delete_file
from marker.convert_single import load_marker


def generate_file_text(response: HtmlResponse):
    filename = generate_file_name_with_url(response=response)
    create_file_pdf(response=response, filename=filename)
    file_text = "load_marker(filename)"
    file_text = "aaaaa bbbbbbb"
    delete_file(filename)
    return file_text
