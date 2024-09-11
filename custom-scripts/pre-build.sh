#!/bin/sh

cp $BASE_DIR/../custom-scripts/hello/hello $BASE_DIR/target/usr/bin
cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/S50hello $BASE_DIR/target/etc/init.d
cp $BASE_DIR/../custom-scripts/trabalho1/tp1.py $BASE_DIR/target/usr/bin
chmod +x $BASE_DIR/target/etc/init.d/S41network-config
chmod +x $BASE_DIR/target/etc/init.d/S50hello
chmod +x $BASE_DIR/target/usr/bin/tp1.py
