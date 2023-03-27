#!/bin/sh -e
set -x

ruff nba_backend tests scripts --fix
black nba_backend tests scripts
isort nba_backend tests scripts