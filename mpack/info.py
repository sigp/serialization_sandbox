#!/usr/bin/env python

################################################################################
# Note:     The current numbers for the max values are rough estimates
#           or placeholders. TODO is to find correct/realistic estimates and
#           provide suitable information.
#
# Note_2:   ``helpers.PLACEHOLDER`` denotes placeholder information that should
#           be changed.
################################################################################

import sys
import os
import argparse
import texttable

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'beacon_chain/'))
sys.path.append(os.path.dirname(sys.path[0]))

from helpers import helpers

from beacon_chain.state.attestation_record import AttestationRecord
from beacon_chain.state.block import Block
from beacon_chain.state.crosslink_record import CrosslinkRecord
from beacon_chain.state.shard_and_committee import ShardAndCommittee
from beacon_chain.state.validator_record import ValidatorRecord
from beacon_chain.state.crystallized_state import CrystallizedState

import messages
import msgpack

verbose = False


def explain_default_size():
    attestation_record = AttestationRecord()
    block = Block()
    crosslink_record = CrosslinkRecord()
    shard_and_committee = ShardAndCommittee()
    crystallized_state = CrystallizedState()

    attestation_record_bytes = msgpack.packb(attestation_record, default=messages.encode_attestation)
    block_bytes = msgpack.packb(block, default=messages.encode_block)
    crosslink_record_bytes = msgpack.packb(crosslink_record, default=messages.encode_crosslink)
    validator_record_bytes = 0
    shard_and_committee_bytes = msgpack.packb(shard_and_committee, default=messages.encode_shard_and_committee)
    crystallized_state_bytes = msgpack.packb(crystallized_state, default=messages.encode_crystallized_state)

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
        'validatorRecord': "N/A",
        'crystallizedState': len(crystallized_state_bytes),
    }


def explain_maxval_size():
    # Attestation Record
    # TODO replace oblique hash loop with correct size
    obl_hashes = []
    for i in range(0, 64):
        obl_hashes.append(helpers.MAX_BYTES)

    attestation_record = AttestationRecord(
        slot=helpers.MAX_I64,
        shard_id=helpers.MAX_I16,
        oblique_parent_hashes=obl_hashes,
        shard_block_hash=helpers.MAX_BYTES,
        attester_bitfield=helpers.MAX_BYTES,
        aggregate_sig=[helpers.MAX_256, helpers.MAX_256]
    )

    # Blocks
    # TODO: provide realistic number for attestations
    attestations = []
    for i in range(0, helpers.MAX_ATTESTATIONS):
        attestations.append(attestation_record)

    block = Block(
        parent_hash=helpers.MAX_BYTES,
        slot_number=helpers.MAX_I64,
        randao_reveal=helpers.MAX_BYTES,
        attestations=attestations,
        pow_chain_ref=helpers.MAX_BYTES,
        active_state_root=helpers.MAX_BYTES,
        crystallized_state_root=helpers.MAX_BYTES,
    )

    # Crosslink Record
    crosslink_record = CrosslinkRecord(
        hash=helpers.MAX_BYTES,
        dynasty=helpers.MAX_I64,
    )

    # Validator Record
    validator_record = ValidatorRecord(
        pubkey=helpers.MAX_256,
        withdrawal_shard=helpers.MAX_I16,
        withdrawal_address=helpers.ADDRESS_BYTES,
        randao_commitment=helpers.MAX_BYTES,
        balance=helpers.MAX_I64,
        start_dynasty=helpers.MAX_I64,
        end_dynasty=helpers.MAX_I64,
    )

    # Shard and Committee
    # TODO: replace placeholder
    committees = []
    for i in range(0, helpers.PLACEHOLDER):
        committees.append(helpers.MAX_I16)

    shard_and_committee = ShardAndCommittee(
        shard_id=helpers.MAX_I16,
        committee=committees,
    )

    # Crystallized State
    validatorlist = []
    for i in range(0, helpers.MAX_VALIDATORS):
        validatorlist.append(validator_record)

    # TODO: replace placeholder
    crosslinklist = []
    for i in range(0, helpers.PLACEHOLDER):
        crosslinklist.append(crosslink_record)

    # TODO: replace placeholder
    indices_heights = []
    for i in range(0, helpers.PLACEHOLDER):
        tmp = []
        for j in range(0, 10):
            tmp.append(shard_and_committee)
        indices_heights.append(tmp)

    crystallized_state = CrystallizedState(
        validators=validatorlist,
        indices_for_heights=indices_heights,
        last_justified_slot=helpers.MAX_I64,
        justified_streak=helpers.MAX_I64,
        last_finalized_slot=helpers.MAX_I64,
        current_dynasty=helpers.MAX_I64,
        crosslinking_start_shard=helpers.MAX_I16,
        crosslink_records=crosslinklist,
        total_deposits=helpers.MAX_256,
        dynasty_seed=helpers.MAX_BYTES,
        dynasty_seed_last_reset=helpers.MAX_I64,
        last_state_recalc=helpers.MAX_I64,
    )

    attestation_record_bytes = msgpack.packb(attestation_record, default=messages.encode_attestation)
    block_bytes = msgpack.packb(block, default=messages.encode_block)
    crosslink_record_bytes = msgpack.packb(crosslink_record, default=messages.encode_crosslink)
    validator_record_bytes = msgpack.packb(validator_record, default=messages.encode_validator_record)
    shard_and_committee_bytes = msgpack.packb(shard_and_committee, default=messages.encode_shard_and_committee)
    crystallized_state_bytes = msgpack.packb(crystallized_state, default=messages.encode_crystallized_state)

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
    parser = argparse.ArgumentParser(description='Testing Cap\'n Proto')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Verbose (Show all prints)')
    args = parser.parse_args()
    verbose = args.verbose

    # Run the experiments
    results = []
    results.append(explain_default_size())
    results.append(explain_maxval_size())

    objects = ['attestationRecord', 'block', 'shardAndCommittee',
               'crosslinkRecord', 'validatorRecord', 'crystallizedState']

    table = texttable.Texttable()
    table.header(['Object', 'Default', 'Maxsize'])

    for item in objects:
        res = [item]
        for r in results:
            res.append(r[item])
        table.add_row(tuple(res))

    output = table.draw()

    print(output)
