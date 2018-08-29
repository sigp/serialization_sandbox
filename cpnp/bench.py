#!/usr/bin/env python

import objects
import capnp
import messages_capnp
import os
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from helpers import helpers


class Serializer_Bench():
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

    def bench_only_serialize(self):
        a_bytes = self.block.to_bytes()
        return a_bytes

    def bench_only_serialize_packed(self):
        a_bytes = self.block.to_bytes_packed()
        return a_bytes

    def bench_create_serialize(self):
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

    # TODO: fix this method; it fails.
    def no_bench_create_serialize_packed(self):
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

    def bench_deserialize(self):
        ar = messages_capnp.Block.from_bytes(self.m_bytes)
        return ar

    # TODO: fix this method; it fails.
    def no_bench_deserialize_packed(self):
        ar = messages_capnp.Block.from_bytes_packed(self.m_packed)
        return ar

    def bench_serialize_deserialize(self):
        a_bytes = self.block.to_bytes()
        ar = messages_capnp.Block.from_bytes(a_bytes)
        return ar

    # TODO: fix this method; it fails.
    def no_bench_serialize_deserialize_packed(self):
        a_bytes = self.block.to_bytes_packed()
        ar = messages_capnp.Block.from_bytes_packed(a_bytes)
        return ar

    def bench_create_serialize_deserialize(self):
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

    # TODO: fix this method; it fails.
    def no_bench_create_serialize_deserialize_packed(self):
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
