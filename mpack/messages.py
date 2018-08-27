################################################################################
# Message encoding and decoding from classes provided by reference
# implementation.
################################################################################

import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'beacon_chain/'))

from beacon_chain.state.attestation_record import AttestationRecord
from beacon_chain.state.block import Block
from beacon_chain.state.crosslink_record import CrosslinkRecord
from beacon_chain.state.shard_and_committee import ShardAndCommittee
from beacon_chain.state.validator_record import ValidatorRecord
from beacon_chain.state.crystallized_state import CrystallizedState

ENDIAN = 'little'

################################################################################
# Encoding
################################################################################

def encode_attestation(attestation):
    if not(isinstance(attestation, AttestationRecord)):
        return None

    return {
        b'slot': attestation.slot,
        b'shard_id': attestation.shard_id,
        b'oblique_parent_hashes': attestation.oblique_parent_hashes,
        b'shard_block_hash': attestation.shard_block_hash,
        b'attester_bitfield': attestation.attester_bitfield,
        b'aggregate_sig': attestation.aggregate_sig,
    }


def encode_block(block):
    if not(isinstance(block, Block)):
        return None

    atts = [encode_attestation(x) for x in block.attestations]

    return {
        b'parent_hash': block.parent_hash,
        b'slot_number': block.slot_number,
        b'randao_reveal': block.randao_reveal,
        b'attestations': atts,
        b'pow_chain_ref': block.pow_chain_ref,
        b'active_state_root': block.active_state_root,
        b'crystallized_state_root': block.crystallized_state_root,
    }


def encode_crosslink(clink):
    if not(isinstance(clink, CrosslinkRecord)):
        return None

    return {
        b'hash': clink.hash,
        b'dynasty': clink.dynasty,
    }


def encode_shard_and_committee(sc):
    if not(isinstance(sc, ShardAndCommittee)):
        return None

    return {
        b'shard_id': sc.shard_id,
        b'committee': sc.committee,
    }


def encode_validator_record(vr):
    if not(isinstance(vr, ValidatorRecord)):
        return None

    return{
        b'pubkey': vr.pubkey,
        b'withdrawal_shard': vr.withdrawal_shard,
        b'withdrawal_address': vr.withdrawal_address,
        b'randao_commitment': vr.randao_commitment,
        b'balance': vr.balance,
        b'start_dynasty': vr.start_dynasty,
        b'end_dynasty': vr.end_dynasty,
    }


def encode_crystallized_state(crystate):
    if not(isinstance(crystate, CrystallizedState)):
        return None

    vrs = [encode_validator_record(v) for v in crystate.validators]
    inh = [[encode_shard_and_committee(y) for y in x] for x in crystate.indices_for_heights]
    cls = [encode_crosslink(c) for c in crystate.crosslink_records]

    return {
        b'validators': vrs,
        b'indices_for_heights': inh,
        b'crosslink_records': cls,
        b'last_justified_slot': crystate.last_justified_slot,
        b'justified_streak': crystate.justified_streak,
        b'last_finalized_slot': crystate.last_finalized_slot,
        b'current_dynasty': crystate.current_dynasty,
        b'crosslinking_start_shard': crystate.crosslinking_start_shard,
        b'total_deposits': crystate.total_deposits,
        b'dynasty_seed': crystate.dynasty_seed,
        b'dynasty_seed_last_reset': crystate. dynasty_seed_last_reset,
        b'last_state_recalc': crystate.last_state_recalc,
    }



################################################################################
# Decode
################################################################################


def decode_attestation(o):
    try:
        a = AttestationRecord(
            slot=o[b'slot'],
            shard_id=o[b'shard_id'],
            oblique_parent_hashes=o[b'oblique_parent_hashes'],
            shard_block_hash=o[b'shard_block_hash'],
            attester_bitfield=o[b'attester_bitfield'],
            aggregate_sig=o[b'aggregate_sig']
        )

        return a
    except KeyError as e:
        print(e)
        return None
