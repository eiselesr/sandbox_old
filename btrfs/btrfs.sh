7#!/bin/bash

#paper mentioned on spinics thread : http://sensille.com/qgroups.pdf

# enable the quota system on the btrfs filesystem
$ sudo btrfs quota enable /apps/

# This command only works inside of a btrfs partition
# I think sub and subvolume are the same
$ sudo btrfs subvolume create test
$ sudo btrfs sub create /apps/test2

# delete subvolume
#https://wiki.archlinux.org/index.php/Btrfs
$ sudo btrfs subvolume delete /apps/test2

# THIS IS THE MOST USEFUL LINK
# https://www.spinics.net/lists/linux-btrfs/msg19457.html
# put limit on subvolume
$ sudo btrfs qgroup limit 2m /apps/test2/

# This has the best examples. It also has scripts to get better btrfs output.
# https://btrfs.wiki.kernel.org/index.php/Quota_support

# I can't seem to get this command to work
#btrfs qgroup create


#run $ df -Th from "$ /". There will be an /app directory of type btrfs.

# detailed information on btfs main filesystem
# $ sudo btrfs filesystem df /apps

# show
sudo btrfs qgroup show /apps/

# delete qgroup. to get the id run show or btrfsQuota.sh (from fabfile.py)
sudo btrfs qgroup destroy /0/210 /apps/test/a

#tool that maybe could be used?
#https://github.com/digint/btrbk/commit/e9a517f161fa4803651dd3ec9855d00ed464e56f
#target_qgroup_destroy
