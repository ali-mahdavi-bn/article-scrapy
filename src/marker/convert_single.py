from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models

configure_logging()
from typing import Optional, List
from backbone.configs import config


def load_marker(filename: str, output: Optional[str] = None, max_pages: int = 10, parallel_factor: int = 6) -> str:
    fname = config.PDF_WEB + filename + ".pdf"
    output_name = output or filename
    model_lst: List = load_all_models()
    full_text, out_meta = convert_single_pdf(fname, model_lst, max_pages=max_pages, parallel_factor=parallel_factor)
    with open(config.OUTPUT_PDF + output_name + ".md", "w+", encoding='utf-8') as f:
        f.write(full_text)
    return full_text
