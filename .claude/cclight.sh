#!/bin/bash
#

DIRNAME="$(dirname $0)"
echo "CMD: $@" >> $DIRNAME/cclight.log
echo "PWD: $(pwd)" >> $DIRNAME/cclight.log

python src/pc/test.py $1