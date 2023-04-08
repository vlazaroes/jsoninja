#!/usr/bin/env bash

set -e
set -x

mypy jsoninja tests
pylint jsoninja tests
black jsoninja tests --check
isort jsoninja tests --check-only
