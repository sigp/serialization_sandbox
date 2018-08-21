#!/usr/bin/bash

# Checking for required files

if [ ! -f `pwd`/pbuf/messages_pb2.py ] || 
    [ ! -f `pwd`/pbuf/packedmessages_pb2.py] ||
    [ ! -d `pwd`/fbuffers/BeaconChain ]; then
    echo "Builds Not Found."
    echo "RUNNING BUILDS"
    ./build.sh
fi

echo '====== GETTING INFORMATION ======'

echo '================================='
echo '========== CAP N PROTO =========='
echo '================================='

python cpnp/info.py

echo '================================='
echo '=========== PROTOBUF ============'
echo '================================='

echo 'NOTE: Protobuf Implementation favours UINTs and does not have max fields.
As such, some discrepancies can be seen.'

python pbuf/info.py


echo '================================='
echo '========== FLATBUFFERS =========='
echo '================================='

echo 'NOTE: The Flatbuffers information file is incomplete.'
python fbuffers/info.py


echo '================================='
echo '===========  SimpleS  ==========='
echo '================================='

python smp/info.py
