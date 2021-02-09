#!/bin/bash

# $1 为文件名，$2 为安装目录
lines=17

filename={FILENAME}
installdir={TARGETDIR}

if [ ! -d "$(installdir)" ]; then
    mkdir installdir
fi

tail -n+$lines $0 > /tmp/$filename

dpkg -i --instdir=$installdir /tmp/$filename
exit 0
