import argparse
import importlib
import inspect
import os

import settings
from articles.domain.mapper import start_mapper
from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from backbone.infrastructure.databases.postgres_connection import DEFAULT_ENGIN
from crawl.crawl import Crawler
from crawl.spider import Spider


def find_subclasses(base_class, module):
    subclasses = []
    if isinstance(base_class, type) and issubclass(module, base_class) and module != base_class:
        subclasses.append(module)
        return subclasses


def get_classes_from_file(file_path, target_class_name):
    module_name, _ = os.path.splitext(os.path.basename(file_path))

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    classes = [
        obj for name, obj in
        inspect.getmembers(module) if
        inspect.isclass(obj) and find_subclasses(Spider, obj) and name == target_class_name]

    return classes


def get_classes_from_directory(directory_path, target_class_name):
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".py"):
            file_path = os.path.join(directory_path, file_name)
            classes_in_file = get_classes_from_file(file_path, target_class_name)
            if classes_in_file:
                return classes_in_file[0]


def lifspan():
    start_mapper()
    MAPPER_REGISTRY.metadata.create_all(DEFAULT_ENGIN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert multiple pdfs to markdown.")
    parser.add_argument("target_class_name", type=str, default=None, help="Metadata json file to use for filtering")
    args = parser.parse_args()
    directories_spider_path = settings.SPIDER_MODULES
    target_class_name = args.target_class_name
    classes_in_directory = ""
    for directory_spider_path in directories_spider_path:
        directory_path = directory_spider_path
        classes_in_directory = get_classes_from_directory(directory_path, target_class_name)
        if classes_in_directory:
            break
    print(classes_in_directory)
    crw = Crawler(lifespan=lifspan)
    crw.start(classes_in_directory)
