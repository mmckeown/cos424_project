#!/bin/bash

# Get script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# All sample theses
THESES=$DIR/sample_theses/*

# Loop over theses and run parse script on them
for f in $THESES
do
    $DIR/parse_ack.py $f
done
