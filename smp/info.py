#!/usr/bin/env python

import sys
import os
import argparse
import texttable

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'helpers'))

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'beacon_chain/'))

import helpers

from beacon_chain.utils.simpleserialize import (
    serialize
)

from beacon_chain.state.attestation_record import AttestationRecord
from beacon_chain.state.block import Block
from beacon_chain.state.crosslink_record import CrosslinkRecord
from beacon_chain.state.shard_and_committee import ShardAndCommittee
from beacon_chain.state.validator_record import ValidatorRecord
from beacon_chain.state.crystallized_state import CrystallizedState

verbose = False


def explain_default_size():
    """
    Show the size of the serialized object with defaults
    Note: ValidatorRecord omitted (has no defaults)
    """
    attestation_record = AttestationRecord()
    block = Block()
    crosslink_record = CrosslinkRecord()
    shard_and_committee = ShardAndCommittee()
    crystallized_state = CrystallizedState()

    attestation_record_bytes = serialize(attestation_record, type(attestation_record))
    block_bytes = serialize(block, type(block))
    crosslink_record_bytes = serialize(crosslink_record, type(crosslink_record))
    shard_and_committee_bytes = serialize(shard_and_committee, type(shard_and_committee))
    crystallized_state_bytes = serialize(crystallized_state, type(crystallized_state))

    if (verbose):
        print('{} | {}'.format(len(attestation_record_bytes), attestation_record_bytes))
        print('{} | {}'.format(len(block_bytes), block_bytes))
        print('{} | {}'.format(len(shard_and_committee_bytes), shard_and_committee_bytes))
        print('{} | {}'.format(len(crosslink_record_bytes), crosslink_record_bytes))
        print('{} | {}'.format(len(crystallized_state_bytes), crystallized_state_bytes))

    return {
        'attestationRecord': len(attestation_record_bytes),
        'block': len(block_bytes),
        'shardAndCommittee': len(shard_and_committee_bytes),
        'crosslinkRecord': len(crosslink_record_bytes),
        'validatorRecord': 0,
        'crystallizedState': len(crystallized_state_bytes),
    }


def explain_maxval_size():
    """
    Show the size of the object when using maximum values
    """

    # Attestation Record
    obl_hashes = []
    for i in range(0, 64):
        obl_hashes.append(b'\xff' * 32)

    agg_sig = []
    for i in range(0, 64):
        agg_sig.append(2**256 - 1)
    attestation_record = AttestationRecord(
        slot=helpers.MAX_I64,
        shard_id=helpers.MAX_I16,
        oblique_parent_hashes=obl_hashes,
        shard_block_hash=helpers.MAX_BYTES,
        attester_bitfield=helpers.MAX_BYTES,
        aggregate_sig=agg_sig
    )

    # Blocks
    attestations = []
    for i in range(0, 2000):
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
        pubkey=(2**256 - 1),
        withdrawal_shard=helpers.MAX_I16,
        withdrawal_address=b'\xff' * 20,
        randao_commitment=helpers.MAX_BYTES,
        balance=helpers.MAX_I64,
        start_dynasty=helpers.MAX_I64,
        end_dynasty=helpers.MAX_I64,
    )

    # Shard and Committee
    committees = []
    for i in range(0, 1000):
        committees.append(helpers.MAX_I16)

    shard_and_committee = ShardAndCommittee(
        shard_id=helpers.MAX_I16,
        committee=committees,
    )

    # Crystallized State
    validatorlist = []
    for i in range(0, 10000):
        validatorlist.append(validator_record)

    crosslinklist = []
    for i in range(0, 1000):
        crosslinklist.append(crosslink_record)

    indices_heights = []
    for i in range(0, 1000):
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
        total_deposits=(2**256 - 1),
        dynasty_seed=helpers.MAX_BYTES,
        dynasty_seed_last_reset=helpers.MAX_I64,
        last_state_recalc=helpers.MAX_I64,
    )

    attestation_record_bytes = serialize(attestation_record, type(attestation_record))
    block_bytes = serialize(block, type(block))
    crosslink_record_bytes = serialize(crosslink_record, type(crosslink_record))
    validator_record_bytes = serialize(validator_record, type(validator_record))
    shard_and_committee_bytes = serialize(shard_and_committee, type(shard_and_committee))
    crystallized_state_bytes = serialize(crystallized_state, type(crystallized_state))

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
