"""
Jsoninja is a library that allows you to generate JSON's from templates written with
Python dicts.
"""

import pytest

from jsoninja import Jsoninja


class TestJsoninja:
    """
    Class that contains the Jsoninja tests.
    """

    def test_no_template_received(self) -> None:
        """
        Tests that an exception is raised when the template is not received.
        """
        jsoninja = Jsoninja()
        with pytest.raises(ValueError, match="A template has not been loaded."):
            jsoninja.replace({}, {})

    def test_returns_new_object(self) -> None:
        """
        Tests that the template is not replaced and returns a new object.
        """
        jsoninja = Jsoninja()
        template = {
            "foo": "{{foo}}",
        }
        replacements = {
            "foo": "bar",
        }
        assert jsoninja.replace(template, replacements) != template

    def test_missing_replacement(self) -> None:
        """
        Tests that an exception is raised when the replacement value of a variable
        declared in the template is not received.
        """
        jsoninja = Jsoninja()
        template = {
            "firstname": "{{firstname}}",
            "lastname": "{{lastname}}",
        }
        replacements = {
            "firstname": "John",
        }
        with pytest.raises(
            KeyError, match='Unable to find a replacement for "lastname".'
        ):
            jsoninja.replace(template, replacements)

    def test_variable_declarations(self) -> None:
        """
        Tests that the variable declarations work correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "declaration1": "{{declaration1}}",
            "declaration2": "{{ declaration2 }}",
        }
        replacements = {
            "declaration1": "foo",
            "declaration2": "bar",
        }
        expected = {
            "declaration1": "foo",
            "declaration2": "bar",
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_str_replacement(self) -> None:
        """
        Tests that the replacement of str variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "str": "{{str}}",
        }
        replacements = {
            "str": "str",
        }
        expected = {
            "str": "str",
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_int_replacement(self) -> None:
        """
        Tests that the replacement of int variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "int": "{{int}}",
        }
        replacements = {
            "int": 1,
        }
        expected = {
            "int": 1,
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_float_replacement(self) -> None:
        """
        Tests that the replacement of float variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "float": "{{float}}",
        }
        replacements = {
            "float": 1.5,
        }
        expected = {
            "float": 1.5,
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_bool_replacement(self) -> None:
        """
        Tests that the replacement of bool variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "bool": "{{bool}}",
        }
        replacements = {
            "bool": True,
        }
        expected = {
            "bool": True,
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_dict_replacement(self) -> None:
        """
        Tests that the replacement of dict variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "dict": "{{dict}}",
        }
        replacements = {
            "dict": {
                "foo": "bar",
            },
        }
        expected = {
            "dict": {
                "foo": "bar",
            },
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_list_replacement(self) -> None:
        """
        Tests that the replacement of list variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "list": "{{list}}",
        }
        replacements = {
            "list": [
                "foo",
                "bar",
            ],
        }
        expected = {
            "list": [
                "foo",
                "bar",
            ],
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_tuple_replacement(self) -> None:
        """
        Tests that the replacement of tuple variables works correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "tuple": "{{tuple}}",
        }
        replacements = {
            "tuple": (
                "foo",
                "bar",
            ),
        }
        expected = {
            "tuple": (
                "foo",
                "bar",
            ),
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_static_values(self) -> None:
        """
        Tests that the static values are working correctly.
        """
        jsoninja = Jsoninja()
        template = {
            "str": "str",
            "int": 1,
            "float": 1.5,
            "bool": True,
            "dict": {
                "foo": "bar",
            },
            "list": [
                "foo",
                "bar",
            ],
            "tuple": (
                "foo",
                "bar",
            ),
            "dynamic": "{{dynamic}}",
        }
        replacements = {
            "dynamic": "dynamic",
        }
        expected = {
            "str": "str",
            "int": 1,
            "float": 1.5,
            "bool": True,
            "dict": {
                "foo": "bar",
            },
            "list": [
                "foo",
                "bar",
            ],
            "tuple": (
                "foo",
                "bar",
            ),
            "dynamic": "dynamic",
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_full_replacement_flow(self) -> None:
        """
        Tests a complete replacement flow.
        """
        jsoninja = Jsoninja()
        template = {
            "firstname": "{{name}}",
            "lastname": "Doe",
            "age": "{{age}}",
            "married": "{{married}}",
            "attributes": "{{attributes}}",
            "hobbies": "{{hobbies}}",
            "languages": "{{languages}}",
        }
        replacements = {
            "name": "John",
            "age": 25,
            "married": False,
            "attributes": {
                "height": 180,
                "weight": 75.5,
            },
            "hobbies": [
                "climbing",
                "videogames",
            ],
            "languages": (
                "english",
                "spanish",
            ),
        }
        expected = {
            "firstname": "John",
            "lastname": "Doe",
            "age": 25,
            "married": False,
            "attributes": {
                "height": 180,
                "weight": 75.5,
            },
            "hobbies": [
                "climbing",
                "videogames",
            ],
            "languages": (
                "english",
                "spanish",
            ),
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_replace_same_variable(self) -> None:
        """
        Tests that a declared variable can be replaced multiple times.
        """
        jsoninja = Jsoninja()
        template = {
            "message1": "{{message}}",
            "message2": "{{message}}",
            "message3": "{{message}}",
        }
        replacements = {
            "message": "I am duplicated!",
        }
        expected = {
            "message1": "I am duplicated!",
            "message2": "I am duplicated!",
            "message3": "I am duplicated!",
        }
        assert jsoninja.replace(template, replacements) == expected

    def test_callback_functions(self) -> None:
        """
        Tests that callback functions can be used from replacements.
        """

        def generate_password() -> str:
            return "super_secret_password"

        jsoninja = Jsoninja()
        template = {
            "password": "{{password}}",
        }
        replacements = {
            "password": generate_password,
        }
        expected = {
            "password": "super_secret_password",
        }
        assert jsoninja.replace(template, replacements) == expected
