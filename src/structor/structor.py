import os.path
import sys
from dataclasses import dataclass
from typing import Dict

import yaml

from .custom_exceptions import CommandDoesNotExist
from .utils import create_dirs_if_not_exists, create_file_if_not_exists, struct_param


@dataclass
class File:
    name: str
    content: str


@dataclass
class Structure:
    commands: dict
    replacement: dict
    file_template: Dict[str, File]


def read_template_if_exists() -> dict:
    """
    Read yaml template if it exists and return a parsed dict
    """
    for template in ['template.yaml', 'template.yml']:
        if os.path.exists(os.path.join(os.getcwd(), f'.structor/{template}')):
            with open(os.path.join(os.getcwd(), f'.structor/{template}')) as tmpl:
                parsed_yaml = yaml.safe_load(tmpl)
                return parsed_yaml


def structure_interpreter(structure_dict: dict, *args) -> Structure:
    """
    Interpret a dict of commands and return a structure object
    :param structure_dict: dict of commands and values to replace
    :param args: args passed through the cli
    :return: structure object with all necessary data
    """

    # Replace args in the dict structure
    replacement = {key: val for key, val in structure_dict.get('replacement').items()}
    if args:
        for index, arg in enumerate(args):
            for key, values in structure_dict.get('replacement').items():
                replacement[key] = values.replace(struct_param(index), args[index])

    # Replace all variables values in the dict structure
    commands = {key: value for key, value in structure_dict.get('commands').items()}
    replaced_commands = {}
    for command, command_value in commands.items():
        replaced_commands[command] = {}
        for path, files in command_value.items():
            for rep, new_rep in replacement.items():
                new_path = path
                if rep in path:
                    new_path = path.replace(rep, new_rep)
                new_files = [file.replace(rep, new_rep) if rep in file else file for file in files]
                replaced_commands[command][new_path] = new_files

    # Replace all variable in file templates
    replaced_file_template = {}
    if structure_dict.get('file-template') is not None:
        file_template = {key: value for key, value in structure_dict.get('file-template').items()}
        for file, tmplt in file_template.items():
            with open(os.path.join(os.getcwd(), f".structor/{tmplt}"), mode='r') as file_content_io:
                file_content = file_content_io.read()
                for rep, new_rep in replacement.items():
                    file_breadcrumb = file.replace(rep, new_rep)
                    file_content = file_content.replace(rep, new_rep)
                file_object = File(name=tmplt, content=file_content)
                replaced_file_template[file_breadcrumb] = file_object

    # Create the structure object
    structure_res = Structure(replaced_commands, replacement, replaced_file_template)
    return structure_res


def generate(structure_obj: Structure, command: str) -> None:
    """
    Generate all the folders and files
    :param structure_obj: structure object with all necessary data
    :param command: all possible command in the cli
    :return: None
    """
    if command not in structure_obj.commands:
        raise CommandDoesNotExist(f"The command {command} does not exist")

    for folders, files in structure_obj.commands.get(command).items():
        path_dirs = os.path.join(os.getcwd(), "/".join(folders.split('>')).replace(" ", ""))
        create_dirs_if_not_exists(path_dirs)
        for file in files:
            create_file_if_not_exists(os.path.join(path_dirs, file))


def run(*args):
    template = read_template_if_exists()
    if template is None:
        from src.structor.base_commands import BASE
        structure = structure_interpreter(BASE, *args[2:])
    else:
        structure = structure_interpreter(template, *args[2:])
    generate(structure, args[1])


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        run(*sys.argv)
