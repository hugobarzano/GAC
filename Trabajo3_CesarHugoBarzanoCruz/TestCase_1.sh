#!/usr/bin/env bash
export GENERATOR_CONFIG=./input/GAC_GENERATOR_CONFIG_1.json
./generadorP3
python ./output/Consumer_class_generated.py
