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