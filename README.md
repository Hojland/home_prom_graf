# home_prom_graf
Prometheus + Grafana stack built with data from micro:bit with attached envirobit sensors (bme280 environment, tcs3472 colour and mems microphone) and external sources


# TODO
- Move sensor sensor files into separate folder (src)
- Make prometheus main script to make webserver that gathers data
- Make sure to save database on mounted device
- Setup whole datahub external part
- Check with Emils source library that everything installed in dockerfile is really necessary


# OBS
- Remember it only runs on python3 
- How does the docker container access the PIs usb port?