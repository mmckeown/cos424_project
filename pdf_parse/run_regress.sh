#!/bin/bash

# Get script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Test set list
TEST_SETS="sample
           test1
           test2
           test3
           test4
           test5
           test6
           test7"

# Run each test set
ALL_PASS=1
for TEST_SET in $TEST_SETS
do
    echo "##############################################"
    echo "# Running Test Set '${TEST_SET}'"
    echo "##############################################"
    ${DIR}/run.sh $TEST_SET
    if [ $? != 0 ]
    then
        ALL_PASS=0
    fi
done

# Output if all tests passed
if [ $ALL_PASS == 1 ]
then
    echo "##############################################"
    echo "# **************ALL TESTS PASS***************#"
    echo "##############################################"
    exit 0
else
    echo "##############################################"
    echo "# *******************FAIL********************#"
    echo "##############################################"
    exit 1
fi
