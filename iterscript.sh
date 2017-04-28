#!/bin/bash

files=`find ../../ml_quality/datasets/shit -name '*.py'` 
for f in $files
do 
 python parser.py $f good_1.out
done


files=`find ../../ml_quality/datasets/fine -name '*.py'` 
for f in $files
do
 python parser.py $f bad_1.out
done

