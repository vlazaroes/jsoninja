<div align="center">
	<p>
        <img src="https://em-content.zobj.net/thumbs/240/apple/354/ninja_1f977.png" width="100px">
    </p>
	<h1>Jsoninja</h1>
    <p>
        <em>
            A library that allows you to generate JSON's from
            <br/>
            templates written with Python data types.
        </em>
    </p>
    <p>
        <img src="https://img.shields.io/pypi/v/jsoninja?label=Version" alt="Library version">
    </p>
</div>

## Instalation

```
$ pip install jsoninja
```

## Use Case Examples

You can use the main Python data types:

```python
import jsoninja

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

Allows multiple replacements of the same variable:

```python
import jsoninja

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
import jsoninja


def generate_password() -> str:
    return "super_secret_password"


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

Support for variables in the dict keys (_replacements must be str, int, float or bool_):

```python
import jsoninja

template = {
    "{{variable_name}}": "bar",
}
replacements = {
    "variable_name": "foo",
}
result = jsoninja.replace(template, replacements)

# {
#   "foo": "bar",
# }
```

If you want to use a custom variable pattern, you can do that too:

```python
from jsoninja import Jsoninja

# The pattern must include a capturing group for the variable name.
pattern = r"\$\{([a-zA-Z0-9_]+)\}"
jsoninja = Jsoninja(variable_pattern=pattern)

template = {
    "foo": "${variable_name}",
}
replacements = {
    "variable_name": "bar",
}
result = jsoninja.replace(template, replacements)

# {
#   "foo": "bar",
# }
```
