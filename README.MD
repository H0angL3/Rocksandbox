# ROCK SANDBOX
**ROCK SANDBOX** được xây dựng dựa trên QEMU với mục đích phục vụ phân tích động mã độc IOT
## Chức năng:
* Thực thi executable file trên qemu-system với kiến trúc tương ứng. (hiện tại chỉ hỗ trợ MIPS).
* Thu thập systemcall thông qua công cụ strace.
* Thu thập hành vi mạng bằng TCPDump
## INSTALL:
### Chuẩn bị:
* Máy ảo Ubuntu desktop 18.04:
  * Network: 2 card m?ng
    * 1 card mạng NAT (ens33)
    * 1 card mạng host only (ens38)
* Tải về qemu image
### Cài đặt QEMU
```
sudo apt-get update
sudo apt-get install qemu
```
### Cài đặt inetsim: 
```
sudo apt-get install inetsim
```
Cấu hình inetsim cho card mạng host only:
```
sudo gedit /etc/inetsim/inetsim.conf
uncomment và sửa lại (default):
service_bind_address	192.168.1.20 
dns_default_ip		192.168.1.20
```

**Tắt apache2 nếu đang chạy:**
```
sudo service apache2 stop
```
### Cài đặt bridge network:
```
sudo apt-get install uml-utilities bridge-utils
groupadd -r tuntap
usermod -a -G tuntap ubuntu (username)
sudo service NetworkManager stop
```
**Sửa interface**
```
sudo gedit /etc/network/interfaces
```
Sửa lại như sau: 
```
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback
atuto ens33
iface ens38 inet dhcp
auto br0
iface br0 inet static
address 192.168.1.20
netmask 255.255.255.0
bridge_ports ens38
bridge_maxwait 0
```
Restart network
```
sudo ifdown -a
sudo ifup -a
```
Kiểm tra với lệnh `ifconfig`, nếu xuất hiện br0 thì OK.
### Cấu hình switch ảo cho QEMU:
```
sudo gedit /etc/qemu-ifup
```
Thêm dòng lệnh switch = br0 như sau:
```
...
switch=$(ip route ls | \
    awk '/^default / {
          for(i=0;i<NF;i++) { if ($i == "dev") { print $(i+1); next; } }
         }'
        )
switch=br0 
...
```
### Cài thư viện cần thiết cho Python3
```
pip3 install paramiko
pip3 install scp
```
## Sử dụng
1. Khởi động qemu với lệnh
```
./run_qemu.sh
```
2. Phân tích sample
```
python3 ./analysis.py -s [sample] -d [destFolder] -t [timeToWait]
```
3. Sau khi phân tích thu được 2 tệp : *strace.txt* và *dump.pcap* tại thư mục [destFolder]




