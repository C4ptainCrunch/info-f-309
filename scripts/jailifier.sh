#!/bin/bash
set -e

#Usage: jailifier.sh netid zip_archive

J=/home/j
JS=/home/js
PATH=$PATH:/usr/local/sbin:/usr/local/bin

# creating jail locations
echo "creating jail locations"
mkdir "$J/$1"
mkdir "$JS/$1"
/usr/local/bin/cpdup "$J/skel" "$JS/$1"

# unzip and send sources to jail
echo unzip and send sources to jail
unzip "$2" -d "$JS/$1/home"
texFile=$(find "$JS/$1/home" -name "*.tex" | head -n 1)
texDir=$(dirname "$texFile")

# mounting jail
echo mounting jail
sudo mount_nullfs -o ro "$J/mroot" "$J/$1"
sudo mount_nullfs -o rw "$JS/$1" "$J/$1/s"
sudo mount -t devfs /dev "$J/$1/dev"

# launching jail
echo launching jail
sudo jail -c path="$J/$1" name="$1" persist

# compiling latex + clamav + moving pdf output #TODO: path
echo compile
sudo jexec "$1" sh -c 'cd ${texDir#$JS/$1} && latexmk -pdf'
echo move "$texDir/"*".pdf" to "/tmp/compile/$1.pdf"
mv "$texDir/"*".pdf" "/tmp/compile/$1.pdf"

# stopping jail + folder deletion
echo stopping jail + folder deletion
sudo jail -r "$1"

sudo umount "$J/$1/dev"
sudo umount "$J/$1/s"
sudo umount "$J/$1"
sudo chflags -R noschg "$JS/$1"
sudo chflags -R noschg "$J/$1"

rm -rf "$JS/$1"
rm -rf "$J/$1"

set +e
