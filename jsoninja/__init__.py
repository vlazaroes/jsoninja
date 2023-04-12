"""
Jsoninja is a library that allows you to generate JSON's from templates written with
Python dicts.
"""

import copy
import re
from typing import Any, Dict, List, Union


class Jsoninja:
    """
    Class that contains the necessary methods of Jsoninja.
    """

    def __init__(self) -> None:
        """
        Initializes the instance with the variable RegEx.
        """
        self.__variable_regex = re.compile(r"\{\{\ ?[a-zA-Z0-9_]+\ ?\}\}")

    def replace(
        self,
        template: Union[List[Dict[str, Any]], Dict[str, Any]],
        replacements: Dict[str, Any],
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
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
        return self.__scan_template(copy.deepcopy(template), replacements)

    def __scan_template(
        self,
        template: Union[List[Dict[str, Any]], Dict[str, Any]],
        replacements: Dict[str, Any],
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Checks if the template is a list or a dict.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A list or a dict containing the template with the replaced values.
        """
        if isinstance(template, list):
            for idx, obj in enumerate(template):
                template[idx] = self.__scan_nodes(obj, replacements)
            return template
        return self.__scan_nodes(template, replacements)

    def __scan_nodes(
        self, template: Dict[str, Any], replacements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Iterate the template and replace the variables with the values.

        Args:
            template (dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A dict containing the template with the replaced values.
        """
        for key, value in template.items():
            if isinstance(value, dict):
                template[key] = self.__scan_nodes(value, replacements)
            else:
                replacement = self.__get_replacement(value, replacements)
                if replacement is not None:
                    if callable(replacement):
                        template[key] = replacement()
                    else:
                        template[key] = replacement
        return template

    def __get_replacement(self, value: Any, replacements: Dict[str, Any]) -> Any:
        """
        Gets the value associated with the template variable.

        Args:
            value (Any): The value of the item.
            replacements (dict): The values to be used as replacements.

        Returns:
            The value associated with the template variable.

        Raises:
            KeyError: Unable to find a replacement for "...".
        """
        if self.__variable_regex.fullmatch(str(value)):
            value_key = self.__clean_value(value)
            if value_key in replacements:
                return replacements[value_key]
            raise KeyError(f'Unable to find a replacement for "{value_key}".')
        return None

    def __clean_value(self, value: str) -> str:
        """
        Removes the brackets that declare the variable from the item value.

        Args:
            value (str): The value of the item.

        Returns:
            The value of the item without the brackets that declare the variable.
        """
        return value[2:-2].strip()
