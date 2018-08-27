#!/usr/bin/env python

################################################################################
# [ NOT PURSUED ]
# Due to the complexity in FlatBuffers surrounding nested structures, we have
# decided to pursue other forms of serialization.
# Factors to leave include:
#   - Size of code required to serialize
#   - Size of bytes produced
#   - Inefficiency of handling nested structures
#
# Please note: this may be revisited at a later stage, or if there are inputs
# from the community, please feel free to work on this :)
################################################################################

################################################################################
# Note:     The current numbers for the max values are rough estimates
#           or placeholders. TODO is to find correct/realistic estimates and
#           provide suitable information.
#
# Note_2:   ``helpers.PLACEHOLDER`` denotes placeholder information that should
#           be changed.
################################################################################

import flatbuffers
import argparse
import texttable

import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'helpers'))
import helpers

# Import the beaconchain flatbuffers message schema
import BeaconChain.Messages
import BeaconChain.Messages.AttestationRecord
import BeaconChain.Messages.Block
import BeaconChain.Messages.CrosslinkRecord
import BeaconChain.Messages.ShardAndCommittee
import BeaconChain.Messages.ShardAndCommitteeArray
import BeaconChain.Messages.ByteArray
import BeaconChain.Messages.CrystallizedState
import BeaconChain.Messages.ValidatorRecord
verbose = False


def explain_default_size():
    """
    Show the size of the object when using default values only
    """

    # Initialise the builders
    attestation_builder = flatbuffers.Builder(0)
    block_builder = flatbuffers.Builder(0)
    crosslink_builder = flatbuffers.Builder(0)
    shard_committee_builder = flatbuffers.Builder(0)
    validator_builder = flatbuffers.Builder(0)
    crystallized_builder = flatbuffers.Builder(0)

    # Build the attestation record
    BeaconChain.Messages.AttestationRecord.AttestationRecordStart(attestation_builder)
    attestation_record = BeaconChain.Messages.AttestationRecord.AttestationRecordEnd(attestation_builder)
    attestation_builder.Finish(attestation_record)
    attestation_record_bytes = attestation_builder.Output()

    # Build the block
    BeaconChain.Messages.Block.BlockStart(block_builder)
    block = BeaconChain.Messages.Block.BlockEnd(block_builder)
    block_builder.Finish(block)
    block_bytes = block_builder.Output()

    # Build the Crosslink Record
    BeaconChain.Messages.CrosslinkRecord.CrosslinkRecordStart(crosslink_builder)
    crosslink_record = BeaconChain.Messages.CrosslinkRecord.CrosslinkRecordEnd(crosslink_builder)
    crosslink_builder.Finish(crosslink_record)
    crosslink_record_bytes = crosslink_builder.Output()

    # Build the Shard And Committee
    BeaconChain.Messages.ShardAndCommittee.ShardAndCommitteeStart(shard_committee_builder)
    shard_and_committee = BeaconChain.Messages.ShardAndCommittee.ShardAndCommitteeEnd(shard_committee_builder)
    shard_committee_builder.Finish(shard_and_committee)
    shard_and_committee_bytes = shard_committee_builder.Output()

    # Build the Validator Record
    BeaconChain.Messages.ValidatorRecord.ValidatorRecordStart(validator_builder)
    validator_record = BeaconChain.Messages.ValidatorRecord.ValidatorRecordEnd(validator_builder)
    validator_builder.Finish(validator_record)
    validator_record_bytes = validator_builder.Output()

    # Build the CrystallizedState
    BeaconChain.Messages.CrystallizedState.CrystallizedStateStart(crystallized_builder)
    crystallized_state = BeaconChain.Messages.CrystallizedState.CrystallizedStateEnd(crystallized_builder)
    crystallized_builder.Finish(crystallized_state)
    crystallized_state_bytes = crystallized_builder.Output()

    if (verbose):
        print('{} | {}'.format(len(attestation_record_bytes), attestation_record_bytes))
        print('{} | {}'.format(len(block_bytes), block_bytes))
        print('{} | {}'.format(len(shard_and_committee_bytes), shard_and_committee_bytes))
        print('{} | {}'.format(len(crosslink_record_bytes), crosslink_record_bytes))
        print('{} | {}'.format(len(validator_record_bytes), validator_record_bytes))
        print('{} | {}'.format(len(crystallized_state_bytes), crystallized_state_bytes))

    return {
        'attestationRecord': len(attestation_record_bytes),
        'block': len(block_bytes),
        'shardAndCommittee': len(shard_and_committee_bytes),
        'crosslinkRecord': len(crosslink_record_bytes),
        'validatorRecord': len(validator_record_bytes),
        'crystallizedState': len(crystallized_state_bytes),
    }


def explain_maxval_size():
    """
    Show the size of the object when using max values
    """

    # Initialise the builders
    attestation_builder = flatbuffers.Builder(0)
    block_builder = flatbuffers.Builder(0)
    crosslink_builder = flatbuffers.Builder(0)
    shard_committee_builder = flatbuffers.Builder(0)
    shard_committee_array_builder = flatbuffers.Builder(0)
    validator_builder = flatbuffers.Builder(0)
    crystallized_builder = flatbuffers.Builder(0)

    # Attestation Record {

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

    # } (End Attestation Record)

    # Build the block
    BeaconChain.Messages.Block.BlockStart(block_builder)
    block = BeaconChain.Messages.Block.BlockEnd(block_builder)
    block_builder.Finish(block)
    block_bytes = block_builder.Output()

    # Build the Crosslink Record
    BeaconChain.Messages.CrosslinkRecord.CrosslinkRecordStart(crosslink_builder)
    crosslink_record = BeaconChain.Messages.CrosslinkRecord.CrosslinkRecordEnd(crosslink_builder)
    crosslink_builder.Finish(crosslink_record)
    crosslink_record_bytes = crosslink_builder.Output()

    # Build the Shard And Committee
    BeaconChain.Messages.ShardAndCommittee.ShardAndCommitteeStart(shard_committee_builder)
    shard_and_committee = BeaconChain.Messages.ShardAndCommittee.ShardAndCommitteeEnd(shard_committee_builder)
    shard_committee_builder.Finish(shard_and_committee)
    shard_and_committee_bytes = shard_committee_builder.Output()

    # Build the Validator Record
    BeaconChain.Messages.ValidatorRecord.ValidatorRecordStart(validator_builder)
    validator_record = BeaconChain.Messages.ValidatorRecord.ValidatorRecordEnd(validator_builder)
    validator_builder.Finish(validator_record)
    validator_record_bytes = validator_builder.Output()

    # Build the CrystallizedState
    BeaconChain.Messages.CrystallizedState.CrystallizedStateStart(crystallized_builder)
    crystallized_state = BeaconChain.Messages.CrystallizedState.CrystallizedStateEnd(crystallized_builder)
    crystallized_builder.Finish(crystallized_state)
    crystallized_state_bytes = crystallized_builder.Output()

    if (verbose):
        print('{} | {}'.format(len(attestation_record_bytes), attestation_record_bytes))
        print('{} | {}'.format(len(block_bytes), block_bytes))
        print('{} | {}'.format(len(shard_and_committee_bytes), shard_and_committee_bytes))
        print('{} | {}'.format(len(crosslink_record_bytes), crosslink_record_bytes))
        print('{} | {}'.format(len(validator_record_bytes), validator_record_bytes))
        print('{} | {}'.format(len(crystallized_state_bytes), crystallized_state_bytes))

    return {
        'attestationRecord': len(attestation_record_bytes),
        'block': len(block_bytes),
        'shardAndCommittee': len(shard_and_committee_bytes),
        'crosslinkRecord': len(crosslink_record_bytes),
        'validatorRecord': len(validator_record_bytes),
        'crystallizedState': len(crystallized_state_bytes),
    }


if (__name__ == '__main__'):

    # Parse the arguments to check verbosity
    parser = argparse.ArgumentParser(description='Testing Flatbuffers')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Verbose (Show all prints)')
    args = parser.parse_args()
    verbose = args.verbose

    results = []
    results.append(explain_default_size())
#   TODO: fix
    results.append(explain_maxval_size())

    objects = ['attestationRecord', 'block', 'shardAndCommittee',
               'crosslinkRecord', 'validatorRecord', 'crystallizedState']

    table = texttable.Texttable()
    table.header(['Object', 'Default', 'Max'])

    for item in objects:
        res = [item]
        for r in results:
            res.append(r[item])
        table.add_row(tuple(res))

    output = table.draw()

    print(output)
