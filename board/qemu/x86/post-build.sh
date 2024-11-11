#!/bin/sh

set -u
set -e

# Add a console on tty1
if [ -e ${TARGET_DIR}/etc/inittab ]; then
    grep -qE '^tty1::' ${TARGET_DIR}/etc/inittab || \
	sed -i '/GENERIC_SERIAL/a\
tty1::respawn:/sbin/getty -L  tty1 0 vt100 # QEMU graphical window' ${TARGET_DIR}/etc/inittab
fi
#Compile the syscall_test.c
BUILDROOT_DIR=$BASE_DIR/..
COMPILER=$BUILDROOT_DIR/output/host/bin/i686-buildroot-linux-gnu-gcc
$COMPILER -o $BUILDROOT_DIR/output/target/bin/syscall_test $BUILDROOT_DIR/custom-scripts/syscall_test.c

# Copiar diskTest (tutorial 2.4) para target
cp $BASE_DIR/../disk-test/diskTest $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/diskTest

# Copiar setPriority e deadline (teste tutorial 3.1) para target
cp $BASE_DIR/../custom-scripts/setpriority-master/setpriority $BASE_DIR/target/usr/bin
cp $BASE_DIR/../custom-scripts/setpriority-master/deadline $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/setpriority
chmod +x $BASE_DIR/target/usr/bin/deadline

# Copiar sched_profiler (trabalho 3) para target
cp $BASE_DIR/../custom-scripts/trabalho3/sched_profiler $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/usr/bin/sched_profiler
