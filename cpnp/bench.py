#!/usr/bin/env python

import timeit
import objects
import capnp
import messages_capnp
import time
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from helpers import helpers

LOOPS = 1
REPEATS = 10**2


class CPNP_Bench():
    def __init__(self):
        messages = objects.MaxVals()

        self.block = messages.block

        self.m_bytes = self.block.to_bytes()
        self.m_packed = self.block.to_bytes_packed()

        self.attest_record_single = messages.attestation_record

        attestRecords = []
        for i in range(0, helpers.MAX_ATTESTATIONS):
            attestRecords.append(self.attest_record_single)

        self.attest_records = attestRecords

    def only_serialize(self):
        a_bytes = self.block.to_bytes()
        return a_bytes

    def only_serialize_packed(self):
        a_bytes = self.block.to_bytes_packed()
        return a_bytes

    def create_serialize(self):
        block = messages_capnp.Block.new_message()
        block.parentHash = helpers.MAX_BYTES
        block.slotNumber = helpers.MAX_U64
        block.randaoReveal = helpers.MAX_BYTES
        block.attestations = self.attest_records
        block.powChainRef = helpers.MAX_BYTES
        block.activateStateRoot: helpers.MAX_BYTES
        block.crystallizedStateRoot = helpers.MAX_BYTES
        a_bytes = block.to_bytes()
        return a_bytes

    def create_serialize_packed(self):
        block = messages_capnp.Block.new_message()
        block.parentHash = helpers.MAX_BYTES
        block.slotNumber = helpers.MAX_U64
        block.randaoReveal = helpers.MAX_BYTES
        block.attestations = self.attest_records
        block.powChainRef = helpers.MAX_BYTES
        block.activateStateRoot: helpers.MAX_BYTES
        block.crystallizedStateRoot = helpers.MAX_BYTES
        a_bytes = block.to_bytes_packed()
        return a_bytes

    def deserialize(self):
        ar = messages_capnp.Block.from_bytes(self.m_bytes)
        return ar

    def deserialize_packed(self):
        ar = messages_capnp.Block.from_bytes_packed(self.m_packed)
        return ar

    def serialize_deserialize(self):
        a_bytes = self.block.to_bytes()
        ar = messages_capnp.Block.from_bytes(a_bytes)
        return ar

    def serialize_deserialize_packed(self):
        a_bytes = self.block.to_bytes_packed()
        ar = messages_capnp.Block.from_bytes_packed(a_bytes)
        return ar

    def create_serialize_deserialize(self):
        block = messages_capnp.Block.new_message()
        block.parentHash = helpers.MAX_BYTES
        block.slotNumber = helpers.MAX_U64
        block.randaoReveal = helpers.MAX_BYTES
        block.attestations = self.attest_records
        block.powChainRef = helpers.MAX_BYTES
        block.activateStateRoot: helpers.MAX_BYTES
        block.crystallizedStateRoot = helpers.MAX_BYTES
        a_bytes = block.to_bytes()
        ar = messages_capnp.Block.from_bytes(a_bytes)
        return ar

    def create_serialize_deserialize_packed(self):
        block = messages_capnp.Block.new_message()
        block.parentHash = helpers.MAX_BYTES
        block.slotNumber = helpers.MAX_U64
        block.randaoReveal = helpers.MAX_BYTES
        block.attestations = self.attest_records
        block.powChainRef = helpers.MAX_BYTES
        block.activateStateRoot: helpers.MAX_BYTES
        block.crystallizedStateRoot = helpers.MAX_BYTES
        a_bytes = block.to_bytes_packed()
        ar = messages_capnp.Block.from_bytes_packed(a_bytes)
        return ar

results = timeit.repeat(
    "bench.only_serialize()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.only_serialize_packed()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.create_serialize()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.create_serialize_packed()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))


results = timeit.repeat(
    "bench.deserialize()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.deserialize_packed()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.serialize_deserialize()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.serialize_deserialize_packed()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.create_serialize_deserialize()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))

results = timeit.repeat(
    "bench.create_serialize_deserialize_packed()",
    setup="from __main__ import CPNP_Bench;bench=CPNP_Bench()",
    repeat=REPEATS,
    timer=time.time,
    number=LOOPS
)

print("LOOPS:\t{}\nREPEAT:\t{}\nAVG:\t{}s".format(LOOPS, REPEATS, (sum(results)/len(results))))
