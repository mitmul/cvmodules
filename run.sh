docker run \
-p 3800$1:8080 \
--name gpu$1 \
--device /dev/nvidia$1 \
--device /dev/nvidiactl \
--device /dev/nvidia-uvm \
-i -d mitmul/cvmodules:1.0 \
/root/start_server
