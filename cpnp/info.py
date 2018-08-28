#!/usr/bin/env python

################################################################################
# Note:     The current numbers for the max values are rough estimates
#           or placeholders. TODO is to find correct/realistic estimates and
#           provide suitable information.
#
# Note_2:   ``helpers.PLACEHOLDER`` denotes placeholder information that should
#           be changed.
################################################################################

import argparse
import texttable
import objects


verbose = False


def explain_default_size(pack=True):
    """
    Show the size of the object when using default values only
    Define whether values should be packed
    """

    messages = objects.Defaults()
    attestation_record = messages.attestation_record
    block = messages.block
    crosslink_record = messages.crosslink_record
    shard_and_committee = messages.shard_and_committee
    validator_record = messages.validator_record
    crystallized_state = messages.crystallized_state

    if(pack):
        attestation_record_bytes = attestation_record.to_bytes_packed()
        block_bytes = block.to_bytes_packed()
        shard_and_committee_bytes = shard_and_committee.to_bytes_packed()
        crosslink_record_bytes = crosslink_record.to_bytes_packed()
        validator_record_bytes = validator_record.to_bytes_packed()
        crystallized_state_bytes = crystallized_state.to_bytes_packed()
    else:
        attestation_record_bytes = attestation_record.to_bytes()
        block_bytes = block.to_bytes()
        shard_and_committee_bytes = shard_and_committee.to_bytes()
        crosslink_record_bytes = crosslink_record.to_bytes()
        validator_record_bytes = validator_record.to_bytes()
        crystallized_state_bytes = crystallized_state.to_bytes()

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
    Show the size of the object when using maximum values
    Define whether packed or unpacked
    """
    messages = objects.MaxVals()
    attestation_record = messages.attestation_record
    block = messages.block
    crosslink_record = messages.crosslink_record
    shard_and_committee = messages.shard_and_committee
    validator_record = messages.validator_record
    crystallized_state = messages.crystallized_state

    if(pack):
        attestation_record_bytes = attestation_record.to_bytes_packed()
        block_bytes = block.to_bytes_packed()
        shard_and_committee_bytes = shard_and_committee.to_bytes_packed()
        crosslink_record_bytes = crosslink_record.to_bytes_packed()
        validator_record_bytes = validator_record.to_bytes_packed()
        crystallized_state_bytes = crystallized_state.to_bytes_packed()
    else:
        attestation_record_bytes = attestation_record.to_bytes()
        block_bytes = block.to_bytes()
        shard_and_committee_bytes = shard_and_committee.to_bytes()
        crosslink_record_bytes = crosslink_record.to_bytes()
        validator_record_bytes = validator_record.to_bytes()
        crystallized_state_bytes = crystallized_state.to_bytes()

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
