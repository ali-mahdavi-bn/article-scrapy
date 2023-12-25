import json
import os
from pathlib import Path
from typing import Dict

current_dir = os.path.dirname(__file__)
root_path_ = Path(current_dir).parent.parent.absolute()

dictionaries = {
    "error": {
        "fa": json.loads(
            Path(root_path_.joinpath(f'api/translator/phrases/{"error"}/{"fa"}.json')).read_text(encoding="utf-8"))
    },
    "enumeration": {
        "fa": json.loads(
            Path(root_path_.joinpath(f'api/translator/phrases/{"enumeration"}/{"fa"}.json')).read_text(
                encoding="utf-8"))
    },
    "entity": {
        "fa": json.loads(
            Path(root_path_.joinpath(f'api/translator/phrases/{"entity"}/{"fa"}.json')).read_text(encoding="utf-8"))
    },
    "resource_access": {
        "fa": json.loads(Path(root_path_.joinpath(f'api/translator/phrases/{"resource_access"}/{"fa"}.json')).read_text(
            encoding="utf-8"))
    },
    "phrases": {
        "fa": json.loads(Path(root_path_.joinpath(f'api/translator/phrases/{"phrases"}/{"fa"}.json')).read_text(
            encoding="utf-8"))
    },
    "function": {
        "fa": json.loads(Path(root_path_.joinpath(f'api/translator/phrases/{"function"}/{"fa"}.json')).read_text(
            encoding="utf-8"))
    },
}  # type: Dict[str, Dict[str, Dict]]


def _get_dictionary(dictionary_type, lang):
    return dictionaries.get(dictionary_type).get(lang)


def translate(phrase: str, **kwargs):
    lang = kwargs.pop("lang") if kwargs.get("lang") else "fa"
    dictionary_type = kwargs.pop("dictionary_type") if kwargs.get("dictionary_type") else "error"
    dictionary = _get_dictionary(dictionary_type, lang)
    if dictionary is None or not phrase or not isinstance(phrase, str):
        return phrase
    translation: str = dictionary.get(phrase) if phrase in dictionary else phrase
    return translation if len(kwargs) == 0 else translation.format(**kwargs)
