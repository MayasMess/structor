import shutil
from unittest import TestCase

from src.structor.structor import structure_interpreter, generate


class TestStructor(TestCase):
    from src.structor.base_commands import BASE

    def setUp(self) -> None:
        pass

    def test_generate(self):
        structure_1 = structure_interpreter(self.BASE, 'hello_app')
        generate(structure_1, 'init')
        generate(structure_1, 'startapp')
        shutil.rmtree('src')

    def test_generate__command_not_exists(self):
        structure_1 = structure_interpreter(self.BASE)
        self.assertRaises(Exception, generate, structure_1, "some_command")

    def test_structure_interpreter(self):
        structure_1 = structure_interpreter(self.BASE, 'my_first_app')
        expected_result = {
            "src > modules > my_first_app": [
                "__init__.py",
                "my_first_app.py",
            ]
        }
        self.assertEqual(expected_result, structure_1.commands.get('startapp'))
