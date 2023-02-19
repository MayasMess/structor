import shutil
from unittest import TestCase

from click import UsageError

from src.structor.structor import structure_interpreter, generate, read_template_if_exists, File


class TestStructor(TestCase):
    from src.structor.base_commands import BASE

    def setUp(self) -> None:
        pass

    def test_generate(self):
        structure_1 = structure_interpreter(self.BASE, ['hello_app'])
        generate(structure_1, 'startapp', ['hello_app'])
        shutil.rmtree('app')

    def test_generate__params_missing(self):
        structure_1 = structure_interpreter(self.BASE, ['hello_app'])
        self.assertRaises(UsageError, generate, structure_1, 'startapp')

    def test_generate__command_not_exists(self):
        structure_1 = structure_interpreter(self.BASE)
        self.assertRaises(Exception, generate, structure_1, "some_command")

    def test_structure_interpreter(self):
        self.BASE['file-template'] = {
            'app > modules > {{APP-NAME}} > {{APP-NAME}}.py': 'my_template_file.py.struct'}
        structure_1 = structure_interpreter(self.BASE, ['my_first_app'])
        expected_result = {
            "app > modules > my_first_app": [
                "__init__.py",
                "my_first_app.py",
                'models.py',
                'views.py',
                'controllers.py'
            ]
        }
        self.assertEqual(expected_result, structure_1.commands.get('startapp'))
        expected_result = {
            'app > modules > my_first_app > my_first_app.py': File('my_template_file.py.struct',
                                                                   'def my_first_app:\n    pass')}
        self.assertEqual(expected_result, structure_1.file_template)

    def test_read_template_if_exists(self):
        result = read_template_if_exists()
        expected_result = self.BASE
        expected_result['file-template'] = {
            'app > modules > {{APP-NAME}} > {{APP-NAME}}.py': 'my_template_file.py.struct'}
        self.assertEqual(result, expected_result)
