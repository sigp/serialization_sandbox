import capnp
import argparse
import texttable

import messages_capnp

verbose = 0

def explain_default_size(pack=True):
    # New messages
    attestation_record= messages_capnp.AttestationRecord.new_message()
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
        crystallized_state_bytes =  crystallized_state.to_bytes_packed()
    else:
        attestation_record_bytes = attestation_record.to_bytes()
        block_bytes = block.to_bytes()
        shard_and_committee_bytes = shard_and_committee.to_bytes()
        crosslink_record_bytes = crosslink_record.to_bytes()
        validator_record_bytes = validator_record.to_bytes()
        crystallized_state_bytes =  crystallized_state.to_bytes()

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
    # Attestation
    attestation_record = messages_capnp.AttestationRecord.new_message()

    attestation_record.slot = 9223372036854775805
    attestation_record.shardId = 6555
    attestation_record.obliqueParentHashes = ['helloworld', 'helloworld', 'helloworld']
    attestation_record.shardBlockHash = b'\xff'*32
    attestation_record.attesterBitfield = b'\xff'*32
    attestation_record.aggregateSig = [b'\xff'*32, b'\xff'*32]

    # Block
    block = messages_capnp.Block.new_message()

    block.parentHash = b'\xff'*32
    block.slotNumber = 9223372036854775805
    block.randaoReveal = b'\xff'*32
    attestRecords = [attestation_record]
    for i in range(0, 100000):
        attestRecords.append(attestation_record)

    block.attestations = attestRecords
    block.powChainRef = b'\xff'*32
    block.activateStateRoot: b'\xff'*32
    block.crystallizedStateRoot = b'\xff'*32

    # Shard and Committee
    shard_and_committee = messages_capnp.ShardAndCommittee.new_message()

    shard_and_committee.shardId = 32767
    committees = []
    for i in range(0, 1000):
        committees.append(2147483647)
    shard_and_committee.committee = committees

    # Crosslink Record
    crosslink_record = messages_capnp.CrosslinkRecord.new_message()

    crosslink_record.dynasty = 9223372036854775805
    crosslink_record.hash = b'\xff'*32



    # ValidatorRecord
    validator_record = messages_capnp.ValidatorRecord.new_message()

    validator_record.pubkey = b'\xff'*32
    validator_record.withdrawalShard = 32767
    validator_record.withdrawalAddress = b'\xff'*32;
    validator_record.randaoCommitment = b'\xff'*32;
    validator_record.balance = 9223372036854775805
    validator_record.startDynasty = 9223372036854775805
    validator_record.endDynasty = 9223372036854775805

    # CrystallizedState

    crystallized_state = messages_capnp.CrystallizedState.new_message()

    validatorlist = []
    for i in range(0, 10000):
        validatorlist.append(validator_record)

    crystallized_state.validators = validatorlist
    crystallized_state.lastStateRecalc = 9223372036854775805

    indices_heights = []
    for i in range(0, 1000):
        tmp = []
        for j in range(0, 10):
            tmp.append(shard_and_committee)
        indices_heights.append(tmp)

    crystallized_state.indicesForHeights = indices_heights
    crystallized_state.lastJustifiedSlot = 9223372036854775805
    crystallized_state.jutifiedStreak = 9223372036854775805
    crystallized_state.lastFinalizedSlot = 9223372036854775805
    crystallized_state.currentDynasty = 9223372036854775805
    crystallized_state.crosslinkingStartShard = 256
    cross_links = []
    for i in range(0, 1000):
        cross_links.append(crosslink_record)
    crystallized_state.crosslinkRecords = cross_links
    crystallized_state.totalDeposits = b'\xff'*32;
    crystallized_state.dynastySeed = b'\xff'*32;
    crystallized_state.dynastySeedLastReset = 9223372036854775805


    if(pack):
        attestation_record_bytes = attestation_record.to_bytes_packed()
        block_bytes = block.to_bytes_packed()
        shard_and_committee_bytes = shard_and_committee.to_bytes_packed()
        crosslink_record_bytes = crosslink_record.to_bytes_packed()
        validator_record_bytes = validator_record.to_bytes_packed()
        crystallized_state_bytes =  crystallized_state.to_bytes_packed()
    else:
        attestation_record_bytes = attestation_record.to_bytes()
        block_bytes = block.to_bytes()
        shard_and_committee_bytes = shard_and_committee.to_bytes()
        crosslink_record_bytes = crosslink_record.to_bytes()
        validator_record_bytes = validator_record.to_bytes()
        crystallized_state_bytes =  crystallized_state.to_bytes()

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

    objects = [ 'attestationRecord', 'block', 'shardAndCommittee',
            'crosslinkRecord', 'validatorRecord', 'crystallizedState' ]

    table = texttable.Texttable()
    table.header(['Object', 'Default (Unpacked)', 'Default (Packed)', 'Maxsize (Unpacked)', 'Maxsize (Packed)'])

    for item in objects:
        res = [item]
        for r in results:
            res.append(r[item])
        table.add_row(tuple(res))

    output = table.draw()

    print(output)




