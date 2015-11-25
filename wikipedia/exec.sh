#!/bin/bash

dir=$1

for filename in $dir/*.json; do
	echo $filename
	python process.py -f $filename --nicks --categories
done
