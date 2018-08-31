#!/usr/bin/env bash
export GENERATOR_CONFIG=./input/GAC_GENERATOR_CONFIG_2.json
./generadorP3
python ./output/Consumer_class_generated.py
python ./output/Gac_models_class_generated.py
