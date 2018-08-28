#!/usr/bin/bash

# Checking for required files

if [ ! -f `pwd`/pbuf/messages_pb2.py ] ||
    [ ! -f `pwd`/pbuf/packedmessages_pb2.py ] ||
    [ ! -d `pwd`/fbuffers/BeaconChain ]; then
    echo "Builds Not Found."
    echo "RUNNING BUILDS"
    ./build.sh
fi

python main.py
