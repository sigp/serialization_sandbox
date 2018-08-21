import capnp
import argparse
import texttable
import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'helpers'))
import helpers

# Import the cap'n proto schema
import messages_capnp

verbose = False


def explain_default_size(pack=True):
    """
    Show the size of the object when using default values only
    Define whether values should be packed
    """

    attestation_record = messages_capnp.AttestationRecord.new_message()
    block = messages_capnp.Block.new_message()
    crosslink_record = messages_capnp.CrosslinkRecord.new_message()
    shard_and_committee = messages_capnp.ShardAndCommittee.new_message()
    validator_record = messages_capnp.ValidatorRecord.new_message()
    crystallized_state = messages_capnp.CrystallizedState.new_message()

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
    # Attestation
    attestation_record = messages_capnp.AttestationRecord.new_message()

    attestation_record.slot = helpers.MAX_U64
    attestation_record.shardId = helpers.MAX_U16
    attestation_record.shardBlockHash = helpers.MAX_BYTES
    attestation_record.attesterBitfield = helpers.MAX_BYTES

    obl_hashes = []
    for i in range(0, 64):
        obl_hashes.append(b'\xff' * 32)

    attestation_record.obliqueParentHashes = obl_hashes

    ag_sig = []
    for i in range(0, 64):
        ag_sig.append(helpers.MAX_BYTES)

    attestation_record.aggregateSig = ag_sig

    # Block
    block = messages_capnp.Block.new_message()

    block.parentHash = helpers.MAX_BYTES
    block.slotNumber = helpers.MAX_U64
    block.randaoReveal = helpers.MAX_BYTES
    attestRecords = []

    for i in range(0, 2000):
        attestRecords.append(attestation_record)

    block.attestations = attestRecords
    block.powChainRef = helpers.MAX_BYTES
    block.activateStateRoot: helpers.MAX_BYTES
    block.crystallizedStateRoot = helpers.MAX_BYTES

    # Shard and Committee
    shard_and_committee = messages_capnp.ShardAndCommittee.new_message()

    shard_and_committee.shardId = helpers.MAX_U16
    committees = []
    for i in range(0, 1000):
        committees.append(helpers.MAX_U32)
    shard_and_committee.committee = committees

    # Crosslink Record
    crosslink_record = messages_capnp.CrosslinkRecord.new_message()

    crosslink_record.dynasty = helpers.MAX_U64
    crosslink_record.hash = helpers.MAX_BYTES

    # ValidatorRecord
    validator_record = messages_capnp.ValidatorRecord.new_message()

    validator_record.pubkey = helpers.MAX_BYTES
    validator_record.withdrawalShard = helpers.MAX_U16
    validator_record.withdrawalAddress = helpers.MAX_BYTES
    validator_record.randaoCommitment = helpers.MAX_BYTES
    validator_record.balance = helpers.MAX_U64
    validator_record.startDynasty = helpers.MAX_U64
    validator_record.endDynasty = helpers.MAX_U64

    # CrystallizedState

    crystallized_state = messages_capnp.CrystallizedState.new_message()

    validatorlist = []
    for i in range(0, 10000):
        validatorlist.append(validator_record)

    crystallized_state.validators = validatorlist
    crystallized_state.lastStateRecalc = helpers.MAX_U64

    indices_heights = []
    for i in range(0, 1000):
        tmp = []
        for j in range(0, 10):
            tmp.append(shard_and_committee)
        indices_heights.append(tmp)

    crystallized_state.indicesForHeights = indices_heights
    crystallized_state.lastJustifiedSlot = helpers.MAX_U64
    crystallized_state.jutifiedStreak = helpers.MAX_U64
    crystallized_state.lastFinalizedSlot = helpers.MAX_U64
    crystallized_state.currentDynasty = helpers.MAX_U64
    crystallized_state.crosslinkingStartShard = helpers.MAX_U16
    cross_links = []
    for i in range(0, 1000):
        cross_links.append(crosslink_record)
    crystallized_state.crosslinkRecords = cross_links
    crystallized_state.totalDeposits = helpers.MAX_BYTES
    crystallized_state.dynastySeed = helpers.MAX_BYTES
    crystallized_state.dynastySeedLastReset = helpers.MAX_U64

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
