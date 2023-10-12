#!/usr/bin/env bash

base=./deb_wiki_mod

function enusre_file_is_executable {
    if [[ -x "$base/main.py" ]]
    then
        : # noop
    else
        chmod +x $base/main.py
    fi
}

function ensure_virtual_env {
    if [ ! -d "./.venv" ]; then
        python3 -m venv .venv
        source ./.venv/bin/activate
        pip install -r requirements.txt
    else
        source ./.venv/bin/activate
    fi
}

function run {
    enusre_file_is_executable
    ensure_virtual_env
    "$base/main.py" $@
}

export PYTHONDONTWRITEBYTECODE=1

run $@

deactivate