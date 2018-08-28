import capnp
import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from helpers import helpers
# Import the cap'n proto schema
import messages_capnp


class Defaults:
    """
    Defines the messages as defaults.
    """
    def __init__(self):
        attestation_record = messages_capnp.AttestationRecord.new_message()
        self.attestation_record = attestation_record
        self.block = messages_capnp.Block.new_message()
        self.crosslink_record = messages_capnp.CrosslinkRecord.new_message()
        self.shard_and_committee = messages_capnp.ShardAndCommittee.new_message()
        self.validator_record = messages_capnp.ValidatorRecord.new_message()
        self.crystallized_state = messages_capnp.CrystallizedState.new_message()


class MaxVals:
    """
    Defines the messages with maximum values for each field
    """
    def __init__(self):
        # Attestation Records
        # TODO replace oblique hash loop with correct size.
        obl_hashes = []
        for i in range(0, 64):
            obl_hashes.append(helpers.MAX_BYTES)

        attestation_record = messages_capnp.AttestationRecord.new_message()
        attestation_record.slot = helpers.MAX_U64
        attestation_record.shardId = helpers.MAX_U16
        attestation_record.shardBlockHash = helpers.MAX_BYTES
        attestation_record.attesterBitfield = helpers.MAX_BYTES
        attestation_record.obliqueParentHashes = obl_hashes
        attestation_record.aggregateSig = [helpers.MAX_BYTES, helpers.MAX_BYTES]

        # Block
        # TODO: provide realistic number for attestations
        attestRecords = []
        for i in range(0, helpers.MAX_ATTESTATIONS):
            attestRecords.append(attestation_record)

        block = messages_capnp.Block.new_message()
        block.parentHash = helpers.MAX_BYTES
        block.slotNumber = helpers.MAX_U64
        block.randaoReveal = helpers.MAX_BYTES
        block.attestations = attestRecords
        block.powChainRef = helpers.MAX_BYTES
        block.activateStateRoot: helpers.MAX_BYTES
        block.crystallizedStateRoot = helpers.MAX_BYTES

        # Shard and Committee
        # TODO: replace placeholder
        committees = []
        for i in range(0, helpers.PLACEHOLDER):
            committees.append(helpers.MAX_U32)

        shard_and_committee = messages_capnp.ShardAndCommittee.new_message()
        shard_and_committee.shardId = helpers.MAX_U16
        shard_and_committee.committee = committees

        # Crosslink Record
        crosslink_record = messages_capnp.CrosslinkRecord.new_message()
        crosslink_record.dynasty = helpers.MAX_U64
        crosslink_record.hash = helpers.MAX_BYTES

        # ValidatorRecord
        validator_record = messages_capnp.ValidatorRecord.new_message()
        validator_record.pubkey = helpers.MAX_BYTES
        validator_record.withdrawalShard = helpers.MAX_U16
        validator_record.withdrawalAddress = helpers.ADDRESS_BYTES
        validator_record.randaoCommitment = helpers.MAX_BYTES
        validator_record.balance = helpers.MAX_U64
        validator_record.startDynasty = helpers.MAX_U64
        validator_record.endDynasty = helpers.MAX_U64

        # CrystallizedState

        validatorlist = []
        for i in range(0, helpers.MAX_VALIDATORS):
            validatorlist.append(validator_record)

        # TODO: replace placeholder
        indices_heights = []
        for i in range(0, helpers.PLACEHOLDER):
            tmp = []
            for j in range(0, 10):
                tmp.append(shard_and_committee)
            indices_heights.append(tmp)

        # TODO: replace placeholder
        cross_links = []
        for i in range(0, helpers.PLACEHOLDER):
            cross_links.append(crosslink_record)

        crystallized_state = messages_capnp.CrystallizedState.new_message()
        crystallized_state.validators = validatorlist
        crystallized_state.lastStateRecalc = helpers.MAX_U64
        crystallized_state.indicesForSlots = indices_heights
        crystallized_state.lastJustifiedSlot = helpers.MAX_U64
        crystallized_state.jutifiedStreak = helpers.MAX_U64
        crystallized_state.lastFinalizedSlot = helpers.MAX_U64
        crystallized_state.currentDynasty = helpers.MAX_U64
        crystallized_state.crosslinkingStartShard = helpers.MAX_U16
        crystallized_state.crosslinkRecords = cross_links
        crystallized_state.totalDeposits = helpers.MAX_BYTES
        crystallized_state.dynastySeed = helpers.MAX_BYTES
        crystallized_state.dynastySeedLastReset = helpers.MAX_U64

        # Save to the class
        self.attestation_record = attestation_record
        self.block = block
        self.shard_and_committee = shard_and_committee
        self.crosslink_record = crosslink_record
        self.validator_record = validator_record
        self.crystallized_state = crystallized_state

