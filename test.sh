#!/usr/bin/bash

echo '====== GETTING INFORMATION ======'

echo '================================='
echo '========== CAP N PROTO =========='
echo '================================='

python cpnp/info.py

echo '================================='
echo '=========== PROTOBUF ============'
echo '================================='

python pbuf/info.py


echo '================================='
echo '========== FLATBUFFERS =========='
echo '================================='

echo 'NOTE: This is incomplete'
sleep 1
python fbuffers/info.py


echo '================================='
echo '===========  SimpleS  ==========='
echo '================================='

python smp/info.py
