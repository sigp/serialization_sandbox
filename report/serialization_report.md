# Understanding Serialization

[Sigma Prime](https://sigmaprime.io)

\* *Note: This is intended to be an extension of the notes on [Ethereum Research Notes](https://notes.ethereum.org/s/BykWongrm).*


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
| [Thrift](https://github.com/facebook/fbthrift)                                                                                 |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |                      | :heavy_check_mark: |                      |                      |
| [Apache Avro](https://avro.apache.org/docs/current/)                                                                           |  :heavy_check_mark:  | :heavy_check_mark: |  :heavy_check_mark:  |  :heavy_check_mark:  | :heavy_check_mark: |                      |                      |

<sup>\*</sup> Offers RPC.\
<sup>\#</sup> Written in Python, currently `106` lines.


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

