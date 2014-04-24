#!/bin/bash

export DISPLAY=':0.0'

DIR='/home/javier/wallpapers/'
WALLPAPER=`ls $DIR | shuf -n 1`

# Change Wallpaper.
feh --bg-fill $DIR$WALLPAPER
