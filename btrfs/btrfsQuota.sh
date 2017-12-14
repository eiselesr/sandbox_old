#!/bin/bash

[[ ! -d $1 ]] && { echo Please pass mountpoint as first argument >&2 ;
exit 1 ; }

while read x i x g x x l x p
do
    volName[i]=$p
done < <(btrfs subvolume list $1)

while read g r e
do
    [[ -z $name ]] && echo -e "subvol\tqgroup\ttotal\tunshared"
    group=${g##*/}
    [[ ! -z ${volName[group]} ]] && name=${volName[group]} || name='(unknown)'
    echo $name $g `numfmt --to=iec $r` `numfmt --to=iec $e`
done < <(btrfs qgroup show --raw $1 | tail -n+3) | column -t
