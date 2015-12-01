docker run \
-p 3000$1:22 \
-p 3800$1:8080 \
--name gpu$1 \
--device /dev/nvidia$1 \
--device /dev/nvidiactl \
--device /dev/nvidia-uvm \
-it mitmul/cvmodules:1.0 \
/bin/bash
