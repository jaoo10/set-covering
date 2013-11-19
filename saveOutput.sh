#!/bin/bash

time=$(date +%s)
initTime=0
file=$(echo $1 | cut -d "/" -f2 | cut -d "." -f1)
file=results/$file
while [ $initTime -le $5 ]
do
    $(./setCovering.py $1 $2 $3 $4 >> $file)
    let initTime=$(date +%s)-$time
done
cat $file | sort > file
cat file > $file
rm file
tac $file
totalLines=$(cat $file | wc -l)
echo "Total: $totalLines"
