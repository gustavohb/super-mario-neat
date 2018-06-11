#!/bin/bash

filename="winner"

while :
do
	if [ -e "$filename" ]
	then
	  break
	fi
	python3 evolve.py
	sleep 2
done

python3 play.py
