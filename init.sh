#!/usr/bin/env bash
set -ex

# clone submodules and update pip packages
git submodule update --init --recursive;
pip install -r finnish_parser/requirements-cpu.txt

# install afinn 
python afinn/setup.py install

# init model files
python finnish_parser/fetch_models.py fi_tdt;
sed -i '.bak' "s/parser_mod/parser_mod --parser-dir=.\/finnish_parser\/Parser-v2/g" models_fi_tdt/pipelines.yaml