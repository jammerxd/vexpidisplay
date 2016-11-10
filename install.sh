#!bin/bash

clear

echo "Now Copying Fonts..."
dir="$(pwd)"
installDir="/usr/share/fonts/truetype"

mkdir $installDir"/NotoSans"
mkdir $installDir"/Liberation"
cp -a $dir"/Fonts/NotoSans/."  $installDir"/NotoSans"
cp -a $dir"/Fonts/Liberation/." $installDir"/Liberation"
chmod -R a+r "/usr/share/fonts/*"
fc-cache -f -v
