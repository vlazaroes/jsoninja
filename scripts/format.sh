#!/usr/bin/env bash

set -x

black jsoninja tests
isort jsoninja tests
