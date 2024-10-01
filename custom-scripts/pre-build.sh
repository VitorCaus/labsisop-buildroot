#!/bin/sh

cp $BASE_DIR/../custom-scripts/hello/hello $BASE_DIR/target/usr/bin
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/S50hello $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/trabalho1/tp1.py $BASE_DIR/target/usr/bin
cp $BASE_DIR/../linux-4.13.9/arch/x86/configs/qemu_x86_custom_defconfig $BASE_DIR/build/arch/x86/configs/qemu_x86_custom_defconfig
chmod +x $BASE_DIR/target/etc/init.d/S41network-config
chmod +x $BASE_DIR/target/etc/init.d/S50hello
chmod +x $BASE_DIR/target/usr/bin/tp1.py
