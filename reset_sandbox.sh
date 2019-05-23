#!/bin/bash
sudo qemu-system-mips -M malta -kernel vmlinux-3.2.0-4-4kc-malta -hda debian_wheezy_rock_ORIGIN_snapshot.img -snapshot -append "root=/dev/sda1 console=tty0" -net nic -net tap
