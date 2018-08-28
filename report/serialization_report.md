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
| validatorRecord        | 7             | 28            | N/A       | 68         | N/A      | N/A                |
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
|         Object         |  Cap'n Proto  |  Flatbuffers* |  MsgPack  |  Protobuf  |  Pickle  |  SimpleSerializer  |
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

<sup>\*</sup> Flatbuffers was abandoned due to the complexity of the code. More
information in the [Discussion](#discussion) section.


# Discussion

## Code Size and Maintainability

One important factor to consider in the selection of techniques is the
maintainability of the code to be implemented. The size of code required to
perform the serialization, as well as how complex the steps are to serialize
and deserialize, should be seen as a critical factor. However, the weight of
this factor should not outweigh performance information, as development can
adapt to implementation.

This is especially targeted towards **Flatbuffers**. Although, during the
preliminary testing, speed was an aspect of Flatbuffers, it was severely
overwhelmed by the complexity and size of the code required for serializing
simple objects.

### Example: Serializing Attestation Records


**Cap'n Proto**:

```python
obl_hashes = []
for i in range(0, 64):
    obl_hashes.append(helpers.MAX_BYTES)

attestation_record = messages_capnp.AttestationRecord.new_message()
attestation_record.slot = helpers.MAX_U64
attestation_record.shardId = helpers.MAX_U16
attestation_record.shardBlockHash = helpers.MAX_BYTES
attestation_record.attesterBitfield = helpers.MAX_BYTES
attestation_record.obliqueParentHashes = obl_hashes
attestation_record.aggregateSig = [helpers.MAX_BYTES, helpers.MAX_BYTES]

```

**Flatbuffers**:

```python

attestation_builder = flatbuffers.Builder(0)
# Shard block hash
BeaconChain.Messages.AttestationRecord.AttestationRecordStartShardBlockHashVector(attestation_builder, 32)
for i in reversed(range(0, 32)):
attestation_builder.PrependByte(255)
shard_block_hash = attestation_builder.EndVector(32)

# Awwwwwer bitfield
BeaconChain.Messages.AttestationRecord.AttestationRecordStartAttesterBitfieldVector(attestation_builder, 32)
for i in reversed(range(0, 32)):
attestation_builder.PrependByte(255)
attester_bitfield = attestation_builder.EndVector(32)

# Oblique parent hashes
obl_hash_bytearrays = []

# Make each byte array
for i in range(0, 64):
# Build the bytes vector for inside the ByteArray (...thanks FlatBuffers for non-nesting capabilities)
BeaconChain.Messages.ByteArray.ByteArrayStartBytesVector(attestation_builder, 32)
for i in reversed(range(0, 32)):
    # b'\xff' equivalent
    attestation_builder.PrependByte(255)
obl_hash_bytes = attestation_builder.EndVector(32)

# Build the byte array
BeaconChain.Messages.ByteArray.ByteArrayStart(attestation_builder)
BeaconChain.Messages.ByteArray.ByteArrayAddBytes(attestation_builder, obl_hash_bytes)
ba = BeaconChain.Messages.ByteArray.ByteArrayEnd(attestation_builder)
obl_hash_bytearrays.append(ba)

# Write the oblique parent hashes to the builder
BeaconChain.Messages.AttestationRecord.AttestationRecordStartObliqueParentHashesVector(attestation_builder, 64)
for i in reversed(range(0, 64)):
attestation_builder.PrependUOffsetTRelative(obl_hash_bytearrays[i])
oblique_parent_hashes = attestation_builder.EndVector(64)

# Aggregate signatures
ag_sig_bytearrays = []

# Make each aggregate signature (0xFF for 32 bytes)
for i in range(0, 2):
# Build the bytes vector for inside the ByteArray (...thanks FlatBuffers for non-nesting capabilities)
BeaconChain.Messages.ByteArray.ByteArrayStartBytesVector(attestation_builder, 32)
for i in reversed(range(0, 32)):
    # b'\xff' equivalent
    attestation_builder.PrependByte(255)
obl_hash_bytes = attestation_builder.EndVector(32)

# Build the byte array
BeaconChain.Messages.ByteArray.ByteArrayStart(attestation_builder)
BeaconChain.Messages.ByteArray.ByteArrayAddBytes(attestation_builder, obl_hash_bytes)
ba = BeaconChain.Messages.ByteArray.ByteArrayEnd(attestation_builder)
ag_sig_bytearrays.append(ba)

# Add the signatures
BeaconChain.Messages.AttestationRecord.AttestationRecordStartAggregateSigVector(attestation_builder, 2)
attestation_builder.PrependUOffsetTRelative(ag_sig_bytearrays[0])
attestation_builder.PrependUOffsetTRelative(ag_sig_bytearrays[1])
aggregate_signature = attestation_builder.EndVector(2)

# Builder
BeaconChain.Messages.AttestationRecord.AttestationRecordStart(attestation_builder)
BeaconChain.Messages.AttestationRecord.AttestationRecordAddSlot(attestation_builder, helpers.MAX_U64)
BeaconChain.Messages.AttestationRecord.AttestationRecordAddShardId(attestation_builder, helpers.MAX_U16)
BeaconChain.Messages.AttestationRecord.AttestationRecordAddShardBlockHash(attestation_builder, shard_block_hash)
BeaconChain.Messages.AttestationRecord.AttestationRecordAddAttesterBitfield(attestation_builder, attester_bitfield)
BeaconChain.Messages.AttestationRecord.AttestationRecordAddObliqueParentHashes(attestation_builder, oblique_parent_hashes)
BeaconChain.Messages.AttestationRecord.AttestationRecordAddAggregateSig(attestation_builder, aggregate_signature)
attestation_record = BeaconChain.Messages.AttestationRecord.AttestationRecordEnd(attestation_builder)
attestation_builder.Finish(attestation_record)
attestation_record_bytes = attestation_builder.Output()

```

A decision was made to leave *FlatBuffers* for this moment with possibility of
returning for further analysis in later stages.



## Compression

To reduce the size of the serialized object, it may be worthwhile discussing
the possibility of adding compression. Compression on the serialized object may
result in smaller amounts of bytes being used in the wire. However, we should
also consider the impact on performance and requirement of extra computation to
reduce the overhead necessary.

There are a number of serialization techniques whose output is suitable for
compressing. This may be leveraged in certain cases to increase bandwidth and
reduce network saturation with high message count.

Such compressions that may be analysed in future:

* bzip
* gzip
* zlib
* lz4


