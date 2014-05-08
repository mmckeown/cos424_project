#!/bin/bash

# Get script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ $# != 1 ]]
then
    echo "Usage: $0 <input dataset>"
    exit
fi

INDATA=$1

# Check input data exists
if [ ! -d ${DIR}/${INDATA}_theses/ ]
then
    echo "No such input dataset '${INDATA}'"
    exit
fi

# All sample theses
THESES=${DIR}/${INDATA}_theses/*.pdf

if [ -e ${DIR}/${INDATA}.out ]
then
    rm ${DIR}/${INDATA}.out
fi

# Loop over theses and run parse script on them
for f in $THESES
do
    $DIR/parse_ack.py $f >> ${DIR}/${INDATA}.out
done

# Diff passing output and current output
diff ${DIR}/${INDATA}.out ${DIR}/${INDATA}_theses/passing_output.out > /dev/null
RET_CODE=$?

# Output pass or fail
if [ $RET_CODE == 0 ]
then
    echo "****PASS*****"
elif [ $RET_CODE == 1 ]
then
    diff ${DIR}/${INDATA}.out ${DIR}/${INDATA}_theses/passing_output.out
    echo "****FAIL****"
else
    echo "Error occured in checking results"
fi
