#!/bin/bash
set -e

#Usage: jailifier.sh netid zip_archive

J=/home/j
JS=/home/js

# creating jail locations
mkdir "$J/$1"
mkdir "$JS/$1"
cpdup "$J/skel" "$JS/$1"

# unzip and send sources to jail
sudo unzip "$2" -d "$JS/$1/home"

# mounting jail
sudo mount_nullfs -o ro "$J/mroot" "$J/$1"
sudo mount_nullfs -o rw "$JS/$1" "$J/$1/s"
sudo mount -t devfs /dev "$J/$1/dev"

# launching jail
sudo jail -c path="$J/$1" name="$1" persist

# compiling latex + clamav + moving pdf output #TODO: path
sudo jexec "$1" sh -c 'cd /home && latexmk -pdf'
mv "$JS/$1/home/"*".pdf" "/tmp/$1.pdf"

# stopping jail + folder deletion
sudo jail -r "$1"

sudo umount "$J/$1/dev"
sudo umount "$J/$1/s"
sudo umount "$J/$1"
sudo chflags -R noschg "$JS/$1"
sudo chflags -R noschg "$J/$1"

rm -rf "$JS/$1"
rm -rf "$J/$1"

set +e
