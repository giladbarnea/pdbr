#!/usr/bin/env bash

EXCLUDED_PATHS="$(find . -mindepth 1 -maxdepth 1 -name '.*' | xargs -I {} basename {} | xargs) venv _build buck-out build dist __pycache__"

function format {
  poetry run nox -r -s lint "$@"
  # or:
  poetry run black --diff --color --exclude "/(${${EXCLUDED_PATHS// /,}//./\.})/" pdbr tests "$@"
}

function check {
  poetry run nox -r -s check "$@"
}

# flake_8 --extend-exclude scratches,docs,log.py
function flake_8 {
  poetry run flake8 --exclude="${EXCLUDED_PATHS// /,}" "$@"
}

function birdseye {
  poetry run python -m birdseye.clear_db && pkill -f birdseye
  poetry run python -m birdseye "$@" &
  sleep 2
  echo '\n'

}

alias nox='command nox --no-stop-on-first-error --reuse-existing-virtualenvs'