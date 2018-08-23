#!/usr/bin/env python

################################################################################
# Note:     The current numbers for the max values are rough estimates
#           or placeholders. TODO is to find correct/realistic estimates and
#           provide suitable information.
#
# Note_2:   ``helpers.PLACEHOLDER`` denotes placeholder information that should
#           be changed.
################################################################################

import messages_pb2
import packedmessages_pb2
import argparse
import texttable
import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'helpers'))
import helpers

verbose = False


def explain_default_size(pack=True):
    """
    Show the size of the object when using default values only
    (UNPACKED)
    """
    # Size of struct with only defaults
    if (pack):
        attestation_record = packedmessages_pb2.PackedAttestationRecord()
    else:
        attestation_record = messages_pb2.AttestationRecord()
    attestation_record.slot = 0
    attestation_record.shard_id = 0
    attestation_record.shard_block_hash = helpers.EMPTY_BYTES
    attestation_record.attester_bitfield = helpers.EMPTY_BYTES
    attestation_record.aggregate_sig.append(0)
    attestation_record.aggregate_sig.append(0)

    if (pack):
        block = packedmessages_pb2.PackedBlock()
    else:
        block = messages_pb2.Block()
    block.parent_hash = helpers.EMPTY_BYTES
    block.slot_number = 0
    block.randao_reveal = helpers.EMPTY_BYTES
    block.pow_chain_ref = helpers.EMPTY_BYTES
    block.active_state_hash = helpers.EMPTY_BYTES
    block.crystallized_state_root = helpers.EMPTY_BYTES

    if (pack):
        shard_and_committee = packedmessages_pb2.PackedShardAndCommittee()
    else:
        shard_and_committee = messages_pb2.ShardAndCommittee()
    shard_and_committee.shard_id = 0

    if (pack):
        crosslink_record = packedmessages_pb2.PackedCrosslinkRecord()
    else:
        crosslink_record = messages_pb2.CrosslinkRecord()
    crosslink_record.dynasty = 0
    crosslink_record.blockhash = helpers.EMPTY_BYTES

    if (pack):
        validator_record = packedmessages_pb2.PackedValidatorRecord()
    else:
        validator_record = messages_pb2.ValidatorRecord()
    validator_record.public_key = 0
    validator_record.withdrawal_shard = 0
    validator_record.withdrawal_address = helpers.EMPTY_BYTES
    validator_record.randao_commitment = helpers.EMPTY_BYTES
    validator_record.balance = 0
    validator_record.start_dynasty = 0
    validator_record.end_dynasty = 0

    if (pack):
        crystallized_state = packedmessages_pb2.PackedCrystallizedState()
    else:
        crystallized_state = messages_pb2.CrystallizedState()
    crystallized_state.last_state_recalc = 0
    crystallized_state.justified_streak = 0
    crystallized_state.last_justified_slot = 0
    crystallized_state.last_finalized_slot = 0
    crystallized_state.current_dynasty = 0
    crystallized_state.crosslinking_start_shard = 0
    crystallized_state.total_deposits = 0
    crystallized_state.dynasty_seed = helpers.EMPTY_BYTES
    crystallized_state.dynasty_seed_last_reset = 0

    attestation_record_bytes = attestation_record.SerializeToString()
    block_bytes = block.SerializeToString()
    shard_and_committee_bytes = shard_and_committee.SerializeToString()
    crosslink_record_bytes = crosslink_record.SerializeToString()
    validator_record_bytes = validator_record.SerializeToString()
    crystallized_state_bytes = crystallized_state.SerializeToString()

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


def explain_maxval_size(pack=True):
    """
    Show the size of the object when using max values
    """
    # Attestation Records
    if (pack):
        attestation_record = packedmessages_pb2.PackedAttestationRecord()
    else:
        attestation_record = messages_pb2.AttestationRecord()
    attestation_record.slot = helpers.MAX_U64
    attestation_record.shard_id = helpers.MAX_U16
    attestation_record.shard_block_hash = helpers.MAX_BYTES
    attestation_record.attester_bitfield = helpers.MAX_BYTES
    attestation_record.aggregate_sig.append(helpers.MAX_U64)
    attestation_record.aggregate_sig.append(helpers.MAX_U64)

    # TODO replace oblique hash loop with correct size.
    for i in range(0, 64):
        attestation_record.oblique_parent_hashes.append(helpers.MAX_BYTES)

    # Blocks
    if (pack):
        block = packedmessages_pb2.PackedBlock()
    else:
        block = messages_pb2.Block()
    block.parent_hash = helpers.MAX_BYTES
    block.slot_number = helpers.MAX_U64
    block.randao_reveal = helpers.MAX_BYTES
    block.pow_chain_ref = helpers.MAX_BYTES
    block.active_state_hash = helpers.MAX_BYTES
    block.crystallized_state_root = helpers.MAX_BYTES

    # TODO: provide realistic number for attestations
    for i in range(0, helpers.MAX_ATTESTATIONS):
        arecord = block.attestations.add()
        arecord.slot = helpers.MAX_U64
        arecord.shard_id = helpers.MAX_U16
        arecord.shard_block_hash = helpers.MAX_BYTES
        arecord.attester_bitfield = helpers.MAX_BYTES
        arecord.aggregate_sig.append(helpers.MAX_U64)
        arecord.aggregate_sig.append(helpers.MAX_U64)
        for i in range(0, 64):
            arecord.oblique_parent_hashes.append(helpers.MAX_BYTES)

    # Shard and Committee
    if (pack):
        shard_and_committee = packedmessages_pb2.PackedShardAndCommittee()
    else:
        shard_and_committee = messages_pb2.ShardAndCommittee()
    shard_and_committee.shard_id = helpers.MAX_U16
    # TODO: replace placeholder
    for i in range(0, helpers.PLACEHOLDER):
        shard_and_committee.committee.append(helpers.MAX_U32)

    # Crosslink Record
    if (pack):
        crosslink_record = packedmessages_pb2.PackedCrosslinkRecord()
    else:
        crosslink_record = messages_pb2.CrosslinkRecord()
    crosslink_record.dynasty = helpers.MAX_U64
    crosslink_record.blockhash = helpers.MAX_BYTES

    # Validator Record
    if(pack):
        validator_record = packedmessages_pb2.PackedValidatorRecord()
    else:
        validator_record = messages_pb2.ValidatorRecord()
    validator_record.public_key = helpers.MAX_U64
    validator_record.withdrawal_shard = helpers.MAX_U16
    validator_record.withdrawal_address = helpers.ADDRESS_BYTES
    validator_record.randao_commitment = helpers.MAX_BYTES
    validator_record.balance = helpers.MAX_U64
    validator_record.start_dynasty = helpers.MAX_U64
    validator_record.end_dynasty = helpers.MAX_U64

    # Crystallized State
    if (pack):
        crystallized_state = packedmessages_pb2.PackedCrystallizedState()
    else:
        crystallized_state = messages_pb2.CrystallizedState()

    crystallized_state.last_state_recalc = helpers.MAX_U64
    crystallized_state.justified_streak = helpers.MAX_U64
    crystallized_state.last_justified_slot = helpers.MAX_U64
    crystallized_state.last_finalized_slot = helpers.MAX_U64
    crystallized_state.current_dynasty = helpers.MAX_U64
    crystallized_state.crosslinking_start_shard = helpers.MAX_U16
    crystallized_state.total_deposits = helpers.MAX_U64
    crystallized_state.dynasty_seed = helpers.MAX_BYTES
    crystallized_state.dynasty_seed_last_reset = helpers.MAX_U64

    # TODO: replace placeholder
    for i in range(0, helpers.PLACEHOLDER):
        crecord = crystallized_state.crosslink_records.add()
        crecord.dynasty = helpers.MAX_U64
        crecord.blockhash = helpers.MAX_BYTES

    for i in range(0, helpers.MAX_VALIDATORS):
        vrecord = crystallized_state.validators.add()
        vrecord.public_key = helpers.MAX_U64
        vrecord.withdrawal_shard = helpers.MAX_U64
        vrecord.withdrawal_address = helpers.ADDRESS_BYTES
        vrecord.randao_commitment = helpers.MAX_BYTES
        vrecord.balance = helpers.MAX_U64
        vrecord.start_dynasty = helpers.MAX_U64
        vrecord.end_dynasty = helpers.MAX_U64

    # TODO: replace placeholder
    for i in range(0, helpers.PLACEHOLDER):
        shard_comittee_array = crystallized_state.indices_for_heights.add()
        for i in range(0, 10):
            scr = shard_comittee_array.array_shard_and_committee.add()
            scr.shard_id = helpers.MAX_U64
            # TODO: replace placeholder
            for i in range(0, helpers.PLACEHOLDER):
                scr.committee.append(helpers.MAX_U32)

    attestation_record_bytes = attestation_record.SerializeToString()
    block_bytes = block.SerializeToString()
    shard_and_committee_bytes = shard_and_committee.SerializeToString()
    crosslink_record_bytes = crosslink_record.SerializeToString()
    validator_record_bytes = validator_record.SerializeToString()
    crystallized_state_bytes = crystallized_state.SerializeToString()

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


if __name__ == '__main__':
    # Parse the arguments to check verbosity
    parser = argparse.ArgumentParser(description='Testing Protobuf')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Verbose (Show all prints)')
    args = parser.parse_args()
    verbose = args.verbose

    results = []
    results.append(explain_default_size(False))
    results.append(explain_default_size(True))
    results.append(explain_maxval_size(False))
    results.append(explain_maxval_size(True))

    objects = ['attestationRecord', 'block', 'shardAndCommittee',
               'crosslinkRecord', 'validatorRecord', 'crystallizedState']

    table = texttable.Texttable()
    table.header(['Object', 'Default (Unpacked)', 'Default (Packed)', 'Maxsize (Unpacked)', 'Maxsize (Packed)'])

    for item in objects:
        res = [item]
        for r in results:
            res.append(r[item])
        table.add_row(tuple(res))

    output = table.draw()

    print(output)
