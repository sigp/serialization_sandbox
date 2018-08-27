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


sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'helpers'))

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'beacon_chain/'))

import helpers

from beacon_chain.state.attestation_record import AttestationRecord
from beacon_chain.state.block import Block
from beacon_chain.state.crosslink_record import CrosslinkRecord
from beacon_chain.state.shard_and_committee import ShardAndCommittee
from beacon_chain.state.validator_record import ValidatorRecord
from beacon_chain.state.crystallized_state import CrystallizedState

import pickle
import struct

verbose = False


def explain_default_size():
    attestation_record = AttestationRecord()
    block = Block()
    crosslink_record = CrosslinkRecord()
    shard_and_committee = ShardAndCommittee()
    crystallized_state = CrystallizedState()

    attestation_record_bytes = pickle.dumps(attestation_record)
    block_bytes = pickle.dumps(block)
    crosslink_record_bytes = pickle.dumps(crosslink_record)
    shard_and_committee_bytes = pickle.dumps(shard_and_committee)
    crystallized_state_bytes = pickle.dumps(crystallized_state)

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
        'validatorRecord': 0,
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
    # results.append(explain_maxval_size())

    objects = ['attestationRecord', 'block', 'shardAndCommittee',
               'crosslinkRecord', 'validatorRecord', 'crystallizedState']

    table = texttable.Texttable()
    table.header(['Object', 'Default'])# , 'Maxsize'])

    for item in objects:
        res = [item]
        for r in results:
            res.append(r[item])
        table.add_row(tuple(res))

    output = table.draw()

    print(output)
