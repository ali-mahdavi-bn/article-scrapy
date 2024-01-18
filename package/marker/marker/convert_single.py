from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models

configure_logging()
from typing import Optional, List
from backbone.configs import config


def load_marker(filename: str, max_pages: int = None, parallel_factor: int = 6) -> str:
    fname = config.PDF_WEB + filename + ".pdf"
    model_lst: List = load_all_models()
    full_text, out_meta = convert_single_pdf(fname, model_lst, max_pages=max_pages, parallel_factor=parallel_factor)

    return full_text
