"""
Jsoninja is a library that allows you to generate JSON's from templates written with
Python data types.
"""

import copy
import re
from typing import Any, Dict, List, Union


class _NoReplacement:
    """
    Class for representing an empty type when there is no replacement.
    """


class Jsoninja:
    """
    Class that contains the necessary methods of Jsoninja.
    """

    def __init__(self) -> None:
        """
        Initializes the instance with the variable RegEx.
        """
        self.__variable_regex = re.compile(r"\{\{\ ?[a-zA-Z0-9_]+\ ?\}\}")
        self.__raise_on_missing = True

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

        Returns:
            A list or a dict containing the template with the replaced values.

        Raises:
            ValueError: A template has not been loaded.
        """
        if not template:
            raise ValueError("A template has not been loaded.")
        self.__raise_on_missing = raise_on_missing
        return self.__scan_template(copy.deepcopy(template), replacements)

    def __scan_template(
        self,
        template: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
    ) -> Union[List[Dict[Any, Any]], Dict[Any, Any]]:
        """
        Checks if the first node of the template is a list or a dict.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A list or a dict containing the template with the replaced values.
        """
        if isinstance(template, list):
            return self.__scan_list(template, replacements)
        return self.__scan_dict(template, replacements)

    def __scan_list(
        self, template: List[Dict[Any, Any]], replacements: Dict[str, Any]
    ) -> List[Dict[Any, Any]]:
        """
        Iterate over the list template.

        Args:
            template (list): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A list containing the template with the replaced values.
        """
        for index, dictionary in enumerate(template):
            self.__scan_node(template, replacements, index, dictionary)
        return template

    def __scan_dict(
        self, template: Dict[Any, Any], replacements: Dict[str, Any]
    ) -> Dict[Any, Any]:
        """
        Iterate over the dict template and stores the key replacements to be replaced.

        Args:
            template (dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A dict containing the template with the replaced values.
        """
        key_replacements: Dict[str, Any] = {}
        for key, value in template.items():
            self.__apply_replacement(key_replacements, replacements, key, key)
            self.__scan_node(template, replacements, key, value)
        self.__replace_keys(template, key_replacements)
        return template

    def __scan_node(
        self,
        template: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
        key: Any,
        value: Any,
    ) -> None:
        """
        Replace the node variables with the corresponding replacements.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            key (Any): The key of the node.
            value (Any): The value of the node.
        """
        if isinstance(value, list):
            self.__scan_list(value, replacements)
        elif isinstance(value, dict):
            template[key] = self.__scan_dict(value, replacements)
        else:
            self.__apply_replacement(template, replacements, key, value)

    def __apply_replacement(
        self,
        structure: Union[List[Dict[Any, Any]], Dict[Any, Any]],
        replacements: Dict[str, Any],
        key: Any,
        variable: Any,
    ) -> None:
        """
        Obtains the replacement of a variable and applies it to the structure.

        Args:
            structure (list | dict): Declares the structure and variables.
            replacements (dict): The values to be used as replacements.
            key (Any): The key of the node.
            variable (Any): The template variable.
        """
        replacement = self.__get_replacement(variable, replacements)
        if not isinstance(replacement, _NoReplacement):
            if callable(replacement):
                structure[key] = replacement()
            else:
                structure[key] = replacement

    def __get_replacement(self, variable: Any, replacements: Dict[str, Any]) -> Any:
        """
        Checks if the received variable is valid and then gets its replacement.

        Args:
            variable (Any): The template variable.
            replacements (dict): The values to be used as replacements.

        Returns:
            The replacement associated for the template variable or None.

        Raises:
            KeyError: Unable to find a replacement for "...".
        """
        replacement: Any = _NoReplacement()
        matches = self.__variable_regex.finditer(str(variable))
        for match in matches:
            var_name = self.__clean_variable(match.group(0))
            if var_name not in replacements:
                if self.__raise_on_missing is False:
                    continue
                raise KeyError(f'Unable to find a replacement for "{var_name}".')
            if match.group(0) == variable:
                return replacements[var_name]
            if isinstance(replacement, _NoReplacement):
                replacement = variable
            replacement = replacement.replace(match.group(0), replacements[var_name])
        return replacement

    def __clean_variable(self, variable: str) -> str:
        """
        Removes the brackets that declare the template variable.

        Args:
            variable (str): The template variable.

        Returns:
            A str with the template variable name without the brackets.
        """
        return variable[2:-2].strip()

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
                value_key = self.__clean_variable(variable)
                raise TypeError(
                    f"Key replacement must be str, int, float or bool ({value_key})."
                )
            template[value] = template.pop(variable)
