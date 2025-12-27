"""
Jsoninja is a library that allows you to generate JSON's from templates written with
Python data types.
"""

import copy
import re
from typing import Any, Dict, List, Optional, Pattern, Union


class _NoReplacement:
    """
    Class for representing an empty type when there is no replacement.
    """


class Jsoninja:
    """
    Class that contains the necessary methods of Jsoninja.
    """

    def __init__(
        self, *, variable_pattern: Optional[Union[str, Pattern[str]]] = None
    ) -> None:
        """
        Initializes the instance with the variable pattern.

        Args:
            variable_pattern (str | Pattern | None): The regex pattern to identify
                template variables.
        """
        if isinstance(variable_pattern, str):
            self.__variable_regex = re.compile(variable_pattern)
            return
        if isinstance(variable_pattern, Pattern):
            self.__variable_regex = variable_pattern
            return
        if variable_pattern is None:
            self.__variable_regex = re.compile(r"\{\{\ ?([a-zA-Z0-9_]+)\ ?\}\}")
            return
        raise TypeError("variable_pattern must be str, Pattern or None.")

    def replace(
        self,
        template: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
        *,
        raise_on_missing: bool = True,
    ) -> Union[List[Dict[Any, Any]], Dict[Any, Any]]:
        """
        Replaces the variables declared in the template.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.

        Returns:
            A list or a dict containing the template with the replaced values.

        Raises:
            ValueError: A template has not been loaded.
        """
        if not template:
            raise ValueError("A template has not been loaded.")
        return self.__scan_template(
            copy.deepcopy(template), replacements, raise_on_missing
        )

    def __scan_template(
        self,
        template: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
        raise_on_missing: bool,
    ) -> Union[List[Dict[Any, Any]], Dict[Any, Any]]:
        """
        Checks if the first node of the template is a list or a dict.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.

        Returns:
            A list or a dict containing the template with the replaced values.
        """
        if isinstance(template, list):
            return self.__scan_list(template, replacements, raise_on_missing)
        return self.__scan_dict(template, replacements, raise_on_missing)

    def __scan_list(
        self,
        template: List[Dict[Any, Any]],
        replacements: Dict[str, Any],
        raise_on_missing: bool,
    ) -> List[Dict[Any, Any]]:
        """
        Iterate over the list template.

        Args:
            template (list): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.

        Returns:
            A list containing the template with the replaced values.
        """
        for index, dictionary in enumerate(template):
            self.__scan_node(
                template, replacements, index, dictionary, raise_on_missing
            )
        return template

    def __scan_dict(
        self,
        template: Dict[Any, Any],
        replacements: Dict[str, Any],
        raise_on_missing: bool,
    ) -> Dict[Any, Any]:
        """
        Iterate over the dict template and stores the key replacements to be replaced.

        Args:
            template (dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.

        Returns:
            A dict containing the template with the replaced values.
        """
        key_replacements: Dict[str, Any] = {}
        for key, value in template.items():
            self.__apply_replacement(
                key_replacements, replacements, key, key, raise_on_missing
            )
            self.__scan_node(template, replacements, key, value, raise_on_missing)
        self.__replace_keys(template, key_replacements)
        return template

    def __scan_node(
        self,
        template: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
        key: Any,
        value: Any,
        raise_on_missing: bool,
    ) -> None:
        """
        Replace the node variables with the corresponding replacements.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            key (Any): The key of the node.
            value (Any): The value of the node.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.
        """
        if isinstance(value, list):
            self.__scan_list(value, replacements, raise_on_missing)
            return
        if isinstance(value, dict):
            template[key] = self.__scan_dict(value, replacements, raise_on_missing)
            return
        self.__apply_replacement(template, replacements, key, value, raise_on_missing)

    def __apply_replacement(
        self,
        structure: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
        key: Any,
        variable: Any,
        raise_on_missing: bool,
    ) -> None:
        """
        Obtains the replacement of a variable and applies it to the structure.

        Args:
            structure (list | dict): Declares the structure and variables.
            replacements (dict): The values to be used as replacements.
            key (Any): The key of the node.
            variable (Any): The template variable.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.
        """
        replacement = self.__get_replacement(variable, replacements, raise_on_missing)
        if isinstance(replacement, _NoReplacement):
            return
        if callable(replacement):
            structure[key] = replacement()
            return
        structure[key] = replacement

    def __get_replacement(
        self,
        variable: Any,
        replacements: Dict[str, Any],
        raise_on_missing: bool,
    ) -> Any:
        """
        Checks if the received variable is valid and then gets its replacement.

        Args:
            variable (Any): The template variable.
            replacements (dict): The values to be used as replacements.
            raise_on_missing (bool): Check if an exception should be thrown when no
                replacement is found.

        Returns:
            The replacement associated for the template variable or None.

        Raises:
            KeyError: Unable to find a replacement for "...".
        """
        replacement: Any = _NoReplacement()
        matches = self.__variable_regex.finditer(str(variable))
        for match in matches:
            variable_name = match.group(1)
            if variable_name not in replacements:
                if raise_on_missing is False:
                    continue
                raise KeyError(f'Unable to find a replacement for "{variable_name}".')
            if match.group(0) == variable:
                return replacements[variable_name]
            if isinstance(replacement, _NoReplacement):
                replacement = variable
            replacement = replacement.replace(
                match.group(0), replacements[variable_name]
            )
        return replacement

    def __replace_keys(
        self, template: Dict[Any, Any], replacements: Dict[str, Any]
    ) -> None:
        """
        Replaces the template variables declared in the keys.

        Args:
            template (dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Raises:
            TypeError: Key replacement must be str, int, float or bool (...).
        """
        for variable, value in replacements.items():
            if not isinstance(value, (str, int, float, bool)):
                match = self.__variable_regex.match(variable)
                value_key = match.group(1) if match and match.groups() else variable
                raise TypeError(
                    f"Key replacement must be str, int, float or bool ({value_key})."
                )
            template[value] = template.pop(variable)


_default_instance = Jsoninja()


def replace(
    template: Union[List[Dict[Any, Any]], Dict[Any, Any]],
    replacements: Dict[str, Any],
    *,
    raise_on_missing: bool = True,
) -> Union[List[Dict[Any, Any]], Dict[Any, Any]]:
    """
    Replaces the variables declared in the template.

    Args:
        template (list | dict): Declares the template structure and variables.
        replacements (dict): The values to be used as replacements.
        raise_on_missing (bool): Check if an exception should be thrown when no
            replacement is found.

    Returns:
        A list or a dict containing the template with the replaced values.

    Raises:
        ValueError: A template has not been loaded.
    """
    return _default_instance.replace(
        template, replacements, raise_on_missing=raise_on_missing
    )
