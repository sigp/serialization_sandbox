#!/usr/bin/bash

# Builds the message schemas for the relevant files

echo 'BUILDING PROTOBUF'

protoc -I=`pwd`/pbuf --python_out=`pwd`/pbuf `pwd`/pbuf/messages.proto
protoc -I=`pwd`/pbuf --python_out=`pwd`/pbuf `pwd`/pbuf/packedmessages.proto

echo 'DONE'

echo 'BUILDING Flatbuffers'

cd ./fbuffers
flatc messages.fbs --python
cd ..

echo 'DONE'

echo 'DONE ALL'

