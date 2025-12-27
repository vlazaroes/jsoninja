"""
Jsoninja is a library that allows you to generate JSON's from templates written with
Python data types.
"""

import re

import pytest

from jsoninja import Jsoninja, replace


def test_variable_pattern_string() -> None:
    """
    Tests that a custom variable pattern can be provided as a string.
    """
    pattern = r"\$\{([a-zA-Z0-9_]+)\}"
    jsoninja = Jsoninja(variable_pattern=pattern)
    template = {
        "foo": "${foo}",
    }
    replacements = {
        "foo": "bar",
    }
    expected = {
        "foo": "bar",
    }
    assert jsoninja.replace(template, replacements) == expected


def test_variable_pattern_compiled() -> None:
    """
    Tests that a custom variable pattern can be provided as a compiled Pattern.
    """
    pattern = re.compile(r"\$\{([a-zA-Z0-9_]+)\}")
    jsoninja = Jsoninja(variable_pattern=pattern)
    template = {
        "foo": "${foo}",
    }
    replacements = {
        "foo": "bar",
    }
    expected = {
        "foo": "bar",
    }
    assert jsoninja.replace(template, replacements) == expected


def test_variable_pattern_invalid_type() -> None:
    """
    Tests that an exception is raised when variable_pattern is not a valid type.
    """
    with pytest.raises(
        TypeError, match=re.escape("variable_pattern must be str, Pattern or None.")
    ):
        Jsoninja(variable_pattern=123)  # type: ignore[arg-type]


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
    expected = [
        {
            "foo": "bar",
        },
    ]
    assert jsoninja.replace(template, replacements) == expected


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
    expected = {
        "foo": "bar",
    }
    assert jsoninja.replace(template, replacements) == expected


def test_variable_declarations() -> None:
    """
    Tests that the different types of variable declarations work correctly.
    """
    jsoninja = Jsoninja()
    template = {
        "without_spaces": "{{type1}}",
        "with_spaces": "{{ type2 }}",
        "multiple_variables": "{{type1}}_{{ type2 }}",
        "{{type1}}": "without_spaces",
        "{{ type2 }}": "with_spaces",
        "{{type1}}_{{ type2 }}": "multiple_variables",
    }
    replacements = {
        "type1": "replacement1",
        "type2": "replacement2",
    }
    expected = {
        "without_spaces": "replacement1",
        "with_spaces": "replacement2",
        "multiple_variables": "replacement1_replacement2",
        "replacement1": "without_spaces",
        "replacement2": "with_spaces",
        "replacement1_replacement2": "multiple_variables",
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
    expected = {
        "firstname": "John",
        "lastname": "{{lastname}}",
    }
    assert jsoninja.replace(template, replacements, raise_on_missing=False) == expected
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


def test_list_replacements() -> None:
    """
    Tests that items can be added to a list with replacements.
    """
    jsoninja = Jsoninja()
    template = {
        "pets": [
            {
                "name": "Qwerty",
                "type": "fish",
            },
            "{{dog}}",
        ]
    }
    replacements = {
        "dog": {
            "name": "Firulais",
            "type": "dog",
        }
    }
    expected = {
        "pets": [
            {
                "name": "Qwerty",
                "type": "fish",
            },
            {
                "name": "Firulais",
                "type": "dog",
            },
        ]
    }
    assert jsoninja.replace(template, replacements) == expected


def test_replace_helper_function() -> None:
    """
    Tests that the replace helper function works correctly using the default instance.
    """
    template = {
        "foo": "{{foo}}",
        "{{foo}}": "foo",
    }
    replacements = {
        "foo": "bar",
    }
    expected = {
        "foo": "bar",
        "bar": "foo",
    }
    assert replace(template, replacements) == expected
