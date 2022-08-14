import shutil
from unittest import TestCase

from src.structor.structor import structure_interpreter, generate, read_template_if_exists, File


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
        self.BASE['file-template'] = {
            'src > modules > {{APP-NAME}} > {{APP-NAME}}.py': 'my_template_file.py.struct'}
        structure_1 = structure_interpreter(self.BASE, 'my_first_app')
        expected_result = {
            "src > modules > my_first_app": [
                "__init__.py",
                "my_first_app.py",
            ]
        }
        self.assertEqual(expected_result, structure_1.commands.get('startapp'))
        expected_result = {
            'src > modules > my_first_app > my_first_app.py': File('my_template_file.py.struct',
                                                                   'def my_first_app:\n    pass')}
        self.assertEqual(expected_result, structure_1.file_template)

    def test_read_template_if_exists(self):
        result = read_template_if_exists()
        expected_result = self.BASE
        expected_result['file-template'] = {
            'src > modules > {{APP-NAME}} > {{APP-NAME}}.py': 'my_template_file.py.struct'}
        self.assertEqual(result, expected_result)
