#!/usr/bin/env bash

set -e
set -x

ruff check jsoninja tests --fix
ruff format jsoninja tests
