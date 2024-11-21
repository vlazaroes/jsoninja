#!/usr/bin/env bash

set -e
set -x

ruff check jsoninja tests
ruff format jsoninja tests --check
mypy jsoninja tests
