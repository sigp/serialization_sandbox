#!/usr/bin/bash

# Checking for required files

if [ ! -f `pwd`/pbuf/messages_pb2.py ] ||
    [ ! -f `pwd`/pbuf/packedmessages_pb2.py ] ||
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
echo 'NOTE_2: Due to complexity of Flatbuffers [it does not like nested
structures at alllll] and the size of attestation record - we are pursuing
different methods. (May be revisited)'
python fbuffers/info.py


echo '================================='
echo '===========  SimpleS  ==========='
echo '================================='

python smp/info.py


echo '================================='
echo '===========  MsgPack  ==========='
echo '================================='

python mpack/info.py

echo '================================='
echo '===========  Pickle   ==========='
echo '================================='

python pythonpickle/info.py
