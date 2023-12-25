import os
from typing import Union

from backbone.configs import config


def delete_file(file: str) -> None:
    try:
        os.remove(config.PDF_WEB + f"{file}.pdf")
        print(f"The file '{file}' has been deleted successfully.")
    except:
        pass
