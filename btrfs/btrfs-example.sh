btrfs sub create a
dd if=/dev/urandom of=a/a1 bs=1M count=10
btrfs sub snap a b
dd if=/dev/urandom of=a/a2 bs=1M count=10
dd if=/dev/urandom of=b/b1 bs=1M count=10
btrfs sub snap a c
dd if=/dev/urandom of=a/a3 bs=1M count=10
dd if=/dev/urandom of=c/c1 bs=1M count=10
btrfs sub snap a d
dd if=/dev/urandom of=a/a4 bs=1M count=10
btrfs sub snap a e
rm a/a1
rm a/a4
sync
