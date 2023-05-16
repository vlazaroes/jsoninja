"""
Jsoninja is a library that allows you to generate JSON's from templates written with
Python data types.
"""

import re

import pytest

from jsoninja import Jsoninja


def test_no_list_template_received() -> None:
    """
    Tests that an exception is raised when the list template is not received.
    """
    jsoninja = Jsoninja()
    with pytest.raises(ValueError, match=re.escape("A template has not been loaded.")):
        jsoninja.replace([], {})


def test_no_dict_template_received() -> None:
    """
    Tests that an exception is raised when the dict template is not received.
    """
    jsoninja = Jsoninja()
    with pytest.raises(ValueError, match=re.escape("A template has not been loaded.")):
        jsoninja.replace({}, {})


def test_returns_new_list_object() -> None:
    """
    Tests that the template is not replaced and returns a new list object.
    """
    jsoninja = Jsoninja()
    template = [
        {
            "foo": "{{foo}}",
        },
    ]
    replacements = {
        "foo": "bar",
    }
    assert jsoninja.replace(template, replacements) != template


def test_returns_new_dict_object() -> None:
    """
    Tests that the template is not replaced and returns a new dict object.
    """
    jsoninja = Jsoninja()
    template = {
        "foo": "{{foo}}",
    }
    replacements = {
        "foo": "bar",
    }
    assert jsoninja.replace(template, replacements) != template


def test_variable_declarations() -> None:
    """
    Tests that the different types of variable declarations work correctly.
    """
    jsoninja = Jsoninja()
    template = {
        "declaration1": "{{type1}}",
        "declaration2": "{{ type2 }}",
        "declaration3": "{{type1}}-{{ type2 }}",
        "{{type1}}": "declaration1",
        "{{ type2 }}": "declaration2",
        "{{type1}}-{{ type2 }}": "declaration3",
    }
    replacements = {
        "type1": "type1",
        "type2": "type2",
    }
    expected = {
        "declaration1": "type1",
        "declaration2": "type2",
        "declaration3": "type1-type2",
        "type1": "declaration1",
        "type2": "declaration2",
        "type1-type2": "declaration3",
    }
    assert jsoninja.replace(template, replacements) == expected


def test_key_replacement_type() -> None:
    """
    Tests that an exception is raised when the replacement value is not a valid type.
    """
    jsoninja = Jsoninja()
    template = {
        "{{str}}": "str",
        "{{int}}": "int",
        "{{float}}": "float",
        "{{bool}}": "bool",
        "{{list}}": "list",
    }
    replacements = {
        "str": "str",
        "int": 0,
        "float": 1.5,
        "bool": True,
        "list": [
            "foo",
            "bar",
        ],
    }
    with pytest.raises(
        TypeError,
        match=re.escape("Key replacement must be str, int, float or bool (list)."),
    ):
        jsoninja.replace(template, replacements)


def test_missing_replacement() -> None:
    """
    Tests that an exception is raised when the replacement value of a variable declared
    in the template is not received.
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
        KeyError, match=re.escape('Unable to find a replacement for "lastname".')
    ):
        jsoninja.replace(template, replacements)


def test_replace_same_variable() -> None:
    """
    Tests that a declared variable can be replaced multiple times with the same
    replacement value.
    """
    jsoninja = Jsoninja()
    template = {
        "message1": "{{message}}",
        "{{message}}": "message2",
        "message3": "{{message}}",
    }
    replacements = {
        "message": "I am duplicated!",
    }
    expected = {
        "message1": "I am duplicated!",
        "I am duplicated!": "message2",
        "message3": "I am duplicated!",
    }
    assert jsoninja.replace(template, replacements) == expected


def test_callback_functions() -> None:
    """
    Tests that callback functions can be used from replacements in templates.
    """

    def generate_password() -> str:
        return "super_secret_password"

    jsoninja = Jsoninja()
    template = {
        "password": "{{password}}",
        "{{password}}": "password",
    }
    replacements = {
        "password": generate_password,
    }
    expected = {
        "password": "super_secret_password",
        "super_secret_password": "password",
    }
    assert jsoninja.replace(template, replacements) == expected


def test_full_replacement_flow() -> None:
    """
    Tests a complete replacement flow.
    """
    jsoninja = Jsoninja()
    template = {
        "firstname": "{{name}}",
        "lastname": "Doe",
        "age": "{{age}}",
        "married": "{{married}}",
        "children": "{{children}}",
        "money": "{{money}}",
        "attributes": "{{attributes}}",
        "hobbies": "{{hobbies}}",
        "pets": [
            {
                "name": "Qwerty",
                "type": "fish",
            },
            "{{pet}}",
        ],
    }
    replacements = {
        "name": "John",
        "age": 25,
        "married": False,
        "children": None,
        "money": 123.45,
        "attributes": {
            "height": 180,
            "weight": 75.5,
        },
        "hobbies": [
            "climbing",
            "videogames",
        ],
        "pet": {
            "name": "Firulais",
            "type": "dog",
        },
    }
    expected = {
        "firstname": "John",
        "lastname": "Doe",
        "age": 25,
        "married": False,
        "children": None,
        "money": 123.45,
        "attributes": {
            "height": 180,
            "weight": 75.5,
        },
        "hobbies": [
            "climbing",
            "videogames",
        ],
        "pets": [
            {
                "name": "Qwerty",
                "type": "fish",
            },
            {
                "name": "Firulais",
                "type": "dog",
            },
        ],
    }
    assert jsoninja.replace(template, replacements) == expected
