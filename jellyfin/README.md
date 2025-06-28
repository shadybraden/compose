# Media server

https://docs.linuxserver.io/images/docker-jellyfin/

---

hardware accel stuff

https://jellyfin.org/docs/general/post-install/transcoding/hardware-acceleration/intel/

N100 supports QSV per: https://github.com/intel/media-driver#supported-platforms

at: https://jellyfin-test.holmlab.org/web/index.html#/dashboard/playback/transcoding
defaults:
h264
vc1
hevc 10bit
vp9 10bit
prefer os native .....
enable hardware encoding

---

enable hwa by adding: (https://docs.linuxserver.io/images/docker-jellyfin/#hardware-acceleration)

        devices:
            - /dev/dri:/dev/dri
 
to compose, then at /web/index.html#/dashboard/playback/transcoding enable QSV and add device=/dev/dri/renderD128

do a `ls /dev/dri` to see your options for device name

boom! a 4k HEVC video went from rendering at ~0.5x speed to over ~1.25x speed wooooooooo