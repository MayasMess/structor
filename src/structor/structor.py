import os.path
import sys
from dataclasses import dataclass

from .custom_exceptions import CommandDoesNotExist
from .utils import create_dirs_if_not_exists, create_file_if_not_exists, struct_param


@dataclass
class Structure:
    commands: dict
    replacement: dict


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
    commands = {key: value for key, value in structure_dict.items() if key != "replacement"}
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

    # Create the structure object
    structure_res = Structure(replaced_commands, replacement)
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


if __name__ == '__main__':
    from src.structor.base_commands import BASE
    if len(sys.argv) >= 2:
        structure = structure_interpreter(BASE, *sys.argv[2:])
        generate(structure, sys.argv[1])
