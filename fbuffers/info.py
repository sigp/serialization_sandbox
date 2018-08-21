#!/usr/bin/env python

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


if (__name__ == '__main__'):

    # Parse the arguments to check verbosity
    parser = argparse.ArgumentParser(description='Testing Flatbuffers')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='Verbose (Show all prints)')
    args = parser.parse_args()
    verbose = args.verbose

    results = []
    results.append(explain_default_size())

    objects = ['attestationRecord', 'block', 'shardAndCommittee',
               'crosslinkRecord', 'validatorRecord', 'crystallizedState']

    table = texttable.Texttable()
    table.header(['Object', 'Default'])

    for item in objects:
        res = [item]
        for r in results:
            res.append(r[item])
        table.add_row(tuple(res))

    output = table.draw()

    print(output)
