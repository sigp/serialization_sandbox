# Serialization Sandbox

A simple playground of different serialization types.

The objective of this repository is to provide a framework to choose different
serialization mechanisms suitable for Ethereum.

## TODOS

* [x] Information Tests
    * Basic structure serialization of default values
    * Basic structure serialization with maximum values
* [ ] Benchmark
    * Time taken to serialize/deserialize default values
    * Time taken to serialize/deserialize max values
    * Benchmark of serialize/deserialize read/write patterns.
* [ ] Profile of operations
    * CPU profiling
    * Memory profiling
* [ ] Summarising report
    * Research and references
    * Overviews
    * Discussion

## Notes

Differences exist between implementations - mainly depiction in each schema
language.

* **AttestationRecord** - aggregate signatures (bytes in Cap'n Proto and
    Simple, Uint64 in Protobuf)
* **Int256** - not depicted in protobuf, as `bytes` in cap'n proto.
* **Int** vs **Uint** - there is discrepancies. The cap'n proto tried to follow
the protobuf implementation and adhere to `Uint`.
* There are some discrepancies between protobuf - it favours uints over some
    fields making it less to serialize.

## Running the tests

### Building the messages

### Using the scripts

Note: running ``./test.sh`` will also check and build files.

```
$ ./build.sh
```

#### Building yourself

**Protobuf** (requires protobuf :
https://developers.google.com/protocol-buffers/ )

```
$ protoc -I=/path/to/repo/pbuf --python_out=/path/to/repo/pbuf /path/to/repo/pbuf/messages.proto

$ protoc -I=/path/to/repo/pbuf --python_out=/path/to/repo/pbuf /path/to/repo/pbuf/packedmessages.proto
```

**FlatBuffers** (reuqires flatbuffers: https://google.github.io/flatbuffers/ )

```
$ cd fbuffers

$ flatc messages.fbs --python
```

### How to run

#### Setup

Install Python deps:

```
$ pip install -r beacon_chain/requirements.txt
```

Ensure git sub-modules are present:

```
$ git submodule init
$ git submodule update
```


#### Running

To run the entire test suite

```
$ ./test.sh
```


**OR**

To run each individual test, it requires python dependencies to be installed
and runs with Python3.

*Note: BeaconChain requirements build with `Python 3.6.6` and will not
compile on `3.7` as of 21/08/2018*

```
$ pip install -r requirements.txt

$ python cpnp/info.py
$ python pbuf/info.py
$ python smp/info.py
...
```


