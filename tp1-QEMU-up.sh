#!/bin/bash

qemu-system-i386 --device e1000,netdev=eth0,mac=aa:bb:cc:dd:ee:ff \
    --netdev user,id=eth0,hostfwd=tcp::8000-:8000 \
    --kernel output/images/bzImage \
    --hda output/images/rootfs.ext2 \
    --nographic --append "console=ttyS0 root=/dev/sda"
