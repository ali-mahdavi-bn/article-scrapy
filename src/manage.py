import sys
from inspect import isclass, getmembers
from typing import Dict, Any, Callable

import settings
from articles.domain.mapper import start_mapper
from backbone.adapter.abstract_data_model import MAPPER_REGISTRY
from backbone.infrastructure.databases.postgres_connection import DEFAULT_ENGIN

CommandArgument = Dict[str, Any]


def lifspan():
    start_mapper()
    # MAPPER_REGISTRY.metadata.create_all(DEFAULT_ENGIN)


def convert_argument_list_to_dict(argument_list: list[str]) -> CommandArgument:
    argument_dict: CommandArgument = {}
    for item in argument_list:
        key, value = item.split(':')
        argument_dict[key] = value
    return argument_dict


def inject_command_to_bus(command_obj: Callable, command_argument: CommandArgument) -> None:
    command = command_obj(**command_argument)
    bus = module.bootstrap.bootstrap()
    bus.handle(command)


def loop_in_commands(module, command_argument: CommandArgument, target_class_name: str) -> None:
    for name_command, command_obj in getmembers(module.domain.commands, isclass):

        if target_class_name == name_command:
            inject_command_to_bus(command_obj, command_argument)


if __name__ == "__main__":

    lifspan()
    args = sys.argv[1:]
    if len(args) < 1:
        raise ValueError("Usage: python script.py <target_class_name> <key1:value1> <key2:value2> ...")

    target_class_name = args[0]
    argument = convert_argument_list_to_dict(args[1:])

    modules_project = settings.MODULES
    for module in modules_project:
        loop_in_commands(module=module, command_argument=argument, target_class_name=target_class_name)
