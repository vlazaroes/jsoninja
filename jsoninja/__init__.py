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
            return self.__scan_list(template, replacements)
        return self.__scan_dict(template, replacements)

    def __scan_list(
        self, template: List[Dict[str, Any]], replacements: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Iterate the list template.

        Args:
            template (list): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A list containing the template with the replaced values.
        """
        for key, value in enumerate(template):
            self.__scan_node(template, replacements, key, value)
        return template

    def __scan_dict(
        self, template: Dict[str, Any], replacements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Iterate the dict template.

        Args:
            template (dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.

        Returns:
            A dict containing the template with the replaced values.
        """
        for key, value in template.items():
            self.__scan_node(template, replacements, key, value)
        return template

    def __scan_node(
        self,
        template: Union[List[Dict[str, Any]], Dict[str, Any]],
        replacements: Dict[str, Any],
        key: Union[int, str],
        value: Any,
    ) -> None:
        """
        Replace the node variables with the values.

        Args:
            template (list | dict): Declares the template structure and variables.
            replacements (dict): The values to be used as replacements.
            key (int | str): The index referring to the position of the node.
            value (Any): The value of the node.
        """
        if isinstance(value, list):
            self.__scan_list(value, replacements)
        elif isinstance(value, dict):
            template[key] = self.__scan_dict(value, replacements)  # type: ignore[index]
        else:
            replacement = self.__get_replacement(value, replacements)
            if replacement is not None:
                if callable(replacement):
                    template[key] = replacement()  # type: ignore[index]
                else:
                    template[key] = replacement  # type: ignore[index]

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
