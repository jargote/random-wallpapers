#!/bin/bash
# Roller
#
# Version 1
#
# Does not sterilize input and such
# Assumes feh is installed

# Change to match the name of the file the script sits in
# Only need to change the script's name once this way

# Change to the directory that contains the images
# /home/user/Pictures/Wallpaper/*
dir="/home/javier/wallpapers/*"

# Counts the number of files in the directory
count=`ls $dir | wc -l`

# Sets a variable for counting the number of files skipped to that point
j=0

# Generates a psuedo-random number
ran_num=$RANDOM

# Sets ran_num to an integer in range:
# 0 to $count - 1
let "ran_num %= $count"

# For all files in the directory
for file in $dir
do
echo $file
# If the file to be used has been found
if [ "$j" -eq "$ran_num" ]
then
# Set the image using feh
feh --bg-center $file
# Break out of the loop: it is done
break

# Appropriate file not found yet: increment and try again
else
let "j++"
fi
done

exit 0
