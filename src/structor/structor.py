import os.path
from dataclasses import dataclass
from typing import Dict, List

import typer
import yaml
from click.exceptions import UsageError, BadParameter

from . import base_commands
from . import utils

app = typer.Typer(pretty_exceptions_show_locals=False)


@dataclass
class File:
    name: str
    content: str


@dataclass
class Structure:
    commands: dict
    replacement: dict
    file_template: Dict[str, File]
    template: dict


def read_template_if_exists() -> dict:
    """
    Read yaml template if it exists and return a parsed dict
    """
    for template in ['template.yaml', 'template.yml']:
        if os.path.exists(os.path.join(os.getcwd(), f'.structor/{template}')):
            with open(os.path.join(os.getcwd(), f'.structor/{template}')) as tmpl:
                parsed_yaml = yaml.safe_load(tmpl)
                return parsed_yaml


def structure_interpreter(structure_dict: dict, args: List[str] = None) -> Structure:
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
                replacement[key] = values.replace(utils.struct_param(index), args[index])

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
    structure_res = Structure(replaced_commands, replacement, replaced_file_template, structure_dict)
    return structure_res


def _get_needed_inner_commands(structure: Structure, command: str) -> List[str]:

    def matching_name(val: str) -> str:
        result = None
        split_1 = val.split('{{')
        if len(split_1) == 2:
            split_2 = split_1[1].split('}}')
            if len(split_2) == 2:
                result = split_2[0]
        return result

    needed_commands = []
    for key, value in structure.template.get('commands').get(command).items():
        needed_command_key = matching_name(key)
        if needed_command_key is not None:
            needed_commands.append(needed_command_key)
        for x in value:
            needed_command_value = matching_name(x)
            if needed_command_value is not None:
                needed_commands.append(needed_command_value)

    return list(set(needed_commands))


def add_content_to_files(structure: Structure):
    if structure.file_template:
        for folder, file in structure.file_template.items():
            with open(os.path.join(os.getcwd(), "/".join(folder.split('>')).replace(" ", "")), mode="w") as f:
                f.write(file.content)


def generate(structure_obj: Structure, command: str, params: List[str] = None) -> None:
    """
    Generate all the folders and files
    :param structure_obj: structure object with all necessary data
    :param command: main command
    :param params: all possible command in the cli
    :return: None
    """
    if params is None:
        params = []
    if command not in structure_obj.commands:
        raise BadParameter(f"The command {params} does not exist")

    needed_commands = _get_needed_inner_commands(structure_obj, command)

    if len(needed_commands) != len(params):
        raise UsageError(f"Matching parameters error... needed => {needed_commands}, given => {params}")

    for folder, files in structure_obj.commands.get(command).items():
        path_dirs = os.path.join(os.getcwd(), "/".join(folder.split('>')).replace(" ", ""))
        utils.create_dirs_if_not_exists(path_dirs)
        for file in files:
            utils.create_file_if_not_exists(os.path.join(path_dirs, file))

    # Add content to file if file_template is added
    add_content_to_files(structure_obj)


@app.command()
def init():
    utils.create_dirs_if_not_exists(f"{os.getcwd()}/.structor")
    with open(f"{os.getcwd()}/.structor/template.yaml", 'w') as yaml_file:
        yaml.dump(base_commands.BASE, yaml_file, default_flow_style=False)


@app.command()
def run(params: List[str]):
    command = params.pop(0)
    template = read_template_if_exists()
    if template is None:
        raise UsageError("Plese run the 'ini' command to generate '.structor/template.yaml' file")
    structure = structure_interpreter(template, params)
    generate(structure, command, params)


def main():
    app()
