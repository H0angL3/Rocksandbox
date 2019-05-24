#!/bin/bash
sudo qemu-system-mips -M malta -kernel ./binary_rocksandbox/vmlinux-3.2.0-4-4kc-malta -hda ./binary_rocksandbox/debian_wheezy_rock_ORIGIN_snapshot.img -snapshot -append "root=/dev/sda1 console=tty0" -net nic -net tap
