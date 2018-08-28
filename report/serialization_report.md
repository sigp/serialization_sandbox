# Understanding Serialization

[Sigma Prime](https://sigmaprime.io)

\* *Note: This is intended to be an extension of the [serialization notes on ethresear.ch](https://notes.ethereum.org/s/BykWongrm).*


This document aims to provide an overview of serialization techniques with the
focus of possible use in the Ethereum 2.0 protocols. We aim to provide an
informative analysis for all techniques as well as provide complimentary
profiling and benchmark information.

This document does not describe in detail each serialization technique, but
provides a high level overview. Furthermore, the experimentation provided is
non-exhaustive, meaning other serialization techniques are available but not
explored and not all objects in the implementation are compared directly.

The objects focused are detailed in [Casper + Sharding Chain
2.1](https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ?view) and are
implemented as close to spec as possible. Discussion of discrepancies features
in the [Discussion](#discussion) section.

# Overview of Serialization Techniques

| Technique                                                                                                                      |          C++         |        Java        |        Python        |          Go          |         C#         |      JavaScript      |         Rust         |
|:-------------------------------------------------------------------------------------------------------------------------------|:--------------------:|:------------------:|:--------------------:|:--------------------:|:------------------:|:--------------------:|:--------------------:|
| [Protobuf](https://developers.google.com/protocol-buffers/)                                                                    |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  |
| [CBOR](http://cbor.io/)                                                                                                        |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  |
| [Cap'n Proto](https://capnproto.org/)<sup>\*</sup>                                                                             | :heavy_check_mark:\* | :heavy_check_mark: | :heavy_check_mark:\* | :heavy_check_mark:\* | :heavy_check_mark: | :heavy_check_mark:\* | :heavy_check_mark:\* |
| [Flatbuffers](https://google.github.io/flatbuffers/)                                                                           |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |                      |
| [SimpleSerialization](https://github.com/ethereum/beacon_chain/blob/master/beacon_chain/utils/simpleserialize.py)<sup>\#</sup> |                      |                    |  :heavy_check_mark:  |                      |                    |                      |                      |
| [MessagePack](https://msgpack.org/index.html)                                                                                  |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  |
| [Thrift](https://github.com/facebook/fbthrift)<sup>\*</sup>                                                                    |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |                      | :heavy_check_mark: |                      |                      |
| [Apache Avro](https://avro.apache.org/docs/current/)                                                                           |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  | :heavy_check_mark: |                      |                      |

<sup>\*</sup> Offers RPC.\
<sup>\#</sup> Written in Python, currently `106` lines.

# Results

## Informative (Byte Size)

The informative results aim to provide information about the serialization in
raw format. This explicitly shows the byte size of each object following
serialization. The `verbose` output of the serialization shows many possible
parts where compression may be advantageous.

### Default Values

```
+-----------------------------------------------------------------------------------------------------------------+
|                                              Info: Default Values                                               |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
|         Object         |  Cap'n Proto  |  Flatbuffers  |  MsgPack  |  Protobuf  |  Pickle  |  SimpleSerializer  |
+========================+===============+===============+===========+============+==========+====================+
| attestationRecord      | 7             | 24            | 128       | 72         | 249      | 122                |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| block                  | 7             | 28            | 285       | 170        | 381      | 176                |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| shardAndCommittee      | 7             | 16            | 22        | 0          | 109      | 10                 |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| crosslinkRecord        | 7             | 16            | 50        | 34         | 131      | 44                 |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| validatorRecord        | 7             | 28            | 0         | 68         | 0        | 0                  |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| crystallizedState      | 7             | 36            | 264       | 34         | 422      | 130                |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
```

The default values are those detailed in the
[spec](https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ?view) and aligned with
the [reference implementation](https://github.com/ethereum/beacon_chain).


### Max Values

This aims to provide insight into an object where all fields are placed as
their maximum values. Insight into this shows that maximum value `uint256` fields
play a major impact on the size of the serialized output.

However, it should be noted that there are discrepancies amongst implementations
for language-specific limitations. [PrysmaticLabs](https://prysmaticlabs.com/) provided
an excellent [**Protobuf**
implementation](https://github.com/prysmaticlabs/prysm/blob/master/proto/beacon/p2p/v1/messages.proto)
of the spec, but different from those implemented
in the reference implementation. The major influence of size difference is
``int256`` vs ``uint64``, which may be an option to *discuss and explore*.


```
+-----------------------------------------------------------------------------------------------------------------+
|                                                Info: Max Values                                                 |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
|         Object         |  Cap'n Proto  |  Flatbuffers  |  MsgPack  |  Protobuf  |  Pickle  |  SimpleSerializer  |
+========================+===============+===============+===========+============+==========+====================+
| attestationRecord      | 2544          | 3312          | 2414      | 2281       | 453      | 2202               |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| block                  | 2.562e+08     | N/A           | 2.414e+08 | 2.284e+08  | 200868   | 2.202e+08          |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| shardAndCommittee      | 4017          | N/A           | 3026      | 5007       | 3112     | 3010               |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| crosslinkRecord        | 53            | N/A           | 58        | 45         | 140      | 44                 |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| validatorRecord        | 134           | N/A           | 183       | 104        | 336      | 114                |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+
| crystallizedState      | 54773684      | N/A           | 48619322  | 61521115   | 236571   | 41548130           |
+------------------------+---------------+---------------+-----------+------------+----------+--------------------+

```


# Discussion

## Code Size

One important factor to consider in the selection of techniques is the
maintainability of the code to be implemented. The size of code required to
perform the serialization, as well as how complex the steps are to serialize
and deserialize, should be seen as a critical factor. However, the weight of
this factor should not outweigh performance information, as development can
adapt to implementation.

## Compression

To reduce the size of the serialized object, it may be worthwhile discussing
the possibility of adding compression. Compression on the serialized object may
result in smaller amounts of bytes being used in the wire. However, we should
also consider the impact on performance and requirement of extra computation to
reduce the overhead necessary.

