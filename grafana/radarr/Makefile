docker create \
  --name=radarr \
    -v <path to data>:/config \
    -v <path to data>:/downloads \
    -v <path to data>:/movies \
    -e PGID=<gid> -e PUID=<uid>  \
    -e TZ=<timezone> \
    -p 7878:7878 \
  lsioarmhf/radarr
