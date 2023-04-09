<div align="center">
	<p>
        <a href="https://pypi.org/project/jsoninja">
            <img src="https://em-content.zobj.net/thumbs/240/apple/354/ninja_1f977.png" width="100px">
        </a>
    </p>
	<h1>Jsoninja</h1>
    <p>
        <em>
            A library that allows you to generate JSON's from
            <br/>
            templates written with Python dicts.
        </em>
    </p>
    <p>
        <a href="https://pypi.org/project/jsoninja">
            <img src="https://img.shields.io/pypi/v/jsoninja?label=Version" alt="Library version">
        </a>
        <a href="https://pypi.org/project/jsoninja">
            <img src="https://img.shields.io/pypi/pyversions/jsoninja.svg?label=Python" alt="Supported Python versions">
        </a>
    </p>
</div>

## Instalation

```
$ pip install jsoninja
```

## Use Case Examples

You can use the main Python data types:

```python
from jsoninja import Jsoninja

jsoninja = Jsoninja()
template = {
    "foo": "{{variable_name}}",
}
replacements = {
    "variable_name": "bar",
}
result = jsoninja.replace(template, replacements)

# {
#   "foo": "bar",
# }
```

Allows multiple substitutions of the same variable:

```python
from jsoninja import Jsoninja

jsoninja = Jsoninja()
template = {
    "message1": "{{message}}",
    "message2": "{{message}}",
    "message3": "{{message}}",
}
replacements = {
    "message": "I am duplicated!",
}
result = jsoninja.replace(template, replacements)

# {
#   "message1": "I am duplicated!",
#   "message2": "I am duplicated!",
#   "message3": "I am duplicated!",
# }
```

Use callback functions to generate the values to be replaced:

```python
from jsoninja import Jsoninja


def generate_password() -> str:
    return "super_secret_password"


jsoninja = Jsoninja()
template = {
    "password": "{{password}}",
}
replacements = {
    "password": generate_password,
}
result = jsoninja.replace(template, replacements)

# {
#   "password": "super_secret_password",
# }
```
