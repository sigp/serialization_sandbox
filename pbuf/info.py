#!/usr/bin/env python
import messages_pb2
import packedmessages_pb2
import argparse
import texttable 

verbose = False

def explain_default_size():
  # Size of struct with only defaults
  attestation_record = messages_pb2.AttestationRecord()
  attestation_record.slot = 0
  attestation_record.shard_id = 0
  attestation_record.shard_block_hash = b'\x00'*32
  attestation_record.attester_bitfield = b'\x00'*32
  attestation_record.aggregate_sig.append(0)
  attestation_record.aggregate_sig.append(0)

  block = messages_pb2.Block()
  block.parent_hash= b'\x00'*32
  block.slot_number= 0
  block.randao_reveal= b'\x00'
  block.pow_chain_ref = b'\x00'*32
  block.active_state_hash = b'\x00'*32
  block.crystallized_state_root = b'\x00'*32

  shard_and_committee = messages_pb2.ShardAndCommittee()
  shard_and_committee.shard_id = 0

  crosslink_record = messages_pb2.CrosslinkRecord()
  crosslink_record.dynasty = 0
  crosslink_record.blockhash = b'\x00'*32

  validator_record = messages_pb2.ValidatorRecord()
  validator_record.public_key = 0
  validator_record.withdrawal_shard = 0
  validator_record.withdrawal_address = b'\x00'*32
  validator_record.randao_commitment = b'\x00'*32
  validator_record.balance = 0
  validator_record.start_dynasty = 0
  validator_record.end_dynasty = 0

  crystallized_state = messages_pb2.CrystallizedState()
  crystallized_state.last_state_recalc = 0
  crystallized_state.justified_streak = 0
  crystallized_state.last_justified_slot = 0
  crystallized_state.last_finalized_slot = 0
  crystallized_state.current_dynasty = 0
  crystallized_state.crosslinking_start_shard = 0
  crystallized_state.total_deposits = 0
  crystallized_state.dynasty_seed = b'\x00'*32
  crystallized_state.dynasty_seed_last_reset = 0


  attestation_record_bytes = attestation_record.SerializeToString()
  block_bytes = block.SerializeToString()
  shard_and_committee_bytes = shard_and_committee.SerializeToString()
  crosslink_record_bytes = crosslink_record.SerializeToString()
  validator_record_bytes = validator_record.SerializeToString()
  crystallized_state_bytes =  crystallized_state.SerializeToString()

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




def explain_default_packed():

  # Size of struct with only defaults
  attestation_record = packedmessages_pb2.PackedAttestationRecord()
  attestation_record.slot = 0
  attestation_record.shard_id = 0
  attestation_record.shard_block_hash = b'\x00'*32
  attestation_record.attester_bitfield = b'\x00'*32
  attestation_record.aggregate_sig.append(0)
  attestation_record.aggregate_sig.append(0)

  block = packedmessages_pb2.PackedBlock()
  block.parent_hash= b'\x00'*32
  block.slot_number= 0
  block.randao_reveal= b'\x00'
  block.pow_chain_ref = b'\x00'*32
  block.active_state_hash = b'\x00'*32
  block.crystallized_state_root = b'\x00'*32

  shard_and_committee = packedmessages_pb2.PackedShardAndCommittee()
  shard_and_committee.shard_id = 0

  crosslink_record = packedmessages_pb2.PackedCrosslinkRecord()
  crosslink_record.dynasty = 0
  crosslink_record.blockhash = b'\x00'*32

  validator_record = packedmessages_pb2.PackedValidatorRecord()
  validator_record.public_key = 0
  validator_record.withdrawal_shard = 0
  validator_record.withdrawal_address = b'\x00'*32
  validator_record.randao_commitment = b'\x00'*32
  validator_record.balance = 0
  validator_record.start_dynasty = 0
  validator_record.end_dynasty = 0

  crystallized_state = packedmessages_pb2.PackedCrystallizedState()
  crystallized_state.last_state_recalc = 0
  crystallized_state.justified_streak = 0
  crystallized_state.last_justified_slot = 0
  crystallized_state.last_finalized_slot = 0
  crystallized_state.current_dynasty = 0
  crystallized_state.crosslinking_start_shard = 0
  crystallized_state.total_deposits = 0
  crystallized_state.dynasty_seed = b'\x00'*32
  crystallized_state.dynasty_seed_last_reset = 0


  attestation_record_bytes = attestation_record.SerializeToString()
  block_bytes = block.SerializeToString()
  shard_and_committee_bytes = shard_and_committee.SerializeToString()
  crosslink_record_bytes = crosslink_record.SerializeToString()
  validator_record_bytes = validator_record.SerializeToString()
  crystallized_state_bytes =  crystallized_state.SerializeToString()

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


def explain_max_size():

  # Size of struct with only defaults
  attestation_record = messages_pb2.AttestationRecord()
  attestation_record.slot = 18446744073709551615
  attestation_record.shard_id = 18446744073709551615
  attestation_record.shard_block_hash = b'\xff'*32
  attestation_record.attester_bitfield = b'\xff'*32
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)

  block = messages_pb2.Block()
  block.parent_hash= b'\xff'*32
  block.slot_number= 18446744073709551615
  block.randao_reveal= b'\xff'
  block.pow_chain_ref = b'\xff'*32
  block.active_state_hash = b'\xff'*32
  block.crystallized_state_root = b'\xff'*32

  shard_and_committee = messages_pb2.ShardAndCommittee()
  shard_and_committee.shard_id = 18446744073709551615
  for i in range(0, 1000):
    shard_and_committee.committee.append(4294967295)

  crosslink_record = messages_pb2.CrosslinkRecord()
  crosslink_record.dynasty = 18446744073709551615
  crosslink_record.blockhash = b'\xff'*32

  validator_record = messages_pb2.ValidatorRecord()
  validator_record.public_key = 18446744073709551615
  validator_record.withdrawal_shard = 18446744073709551615
  validator_record.withdrawal_address = b'\xff'*32
  validator_record.randao_commitment = b'\xff'*32
  validator_record.balance = 18446744073709551615
  validator_record.start_dynasty = 18446744073709551615
  validator_record.end_dynasty = 18446744073709551615

  crystallized_state = messages_pb2.CrystallizedState()
  crystallized_state.last_state_recalc = 18446744073709551615
  crystallized_state.justified_streak = 18446744073709551615
  crystallized_state.last_justified_slot = 18446744073709551615
  crystallized_state.last_finalized_slot = 18446744073709551615
  crystallized_state.current_dynasty = 18446744073709551615
  crystallized_state.crosslinking_start_shard = 18446744073709551615
  crystallized_state.total_deposits = 18446744073709551615
  crystallized_state.dynasty_seed = b'\xff'*32
  crystallized_state.dynasty_seed_last_reset = 18446744073709551615


  for i in range(0, 1000):
    crecord = crystallized_state.crosslink_records.add()
    crecord.dynasty = 18446744073709551615
    crecord.blockhash = b'\xff'*32

  for i in range(0, 1000):
    vrecord = crystallized_state.validators.add()
    vrecord.public_key = 18446744073709551615
    vrecord.withdrawal_shard = 18446744073709551615
    vrecord.withdrawal_address = b'\xff'*32
    vrecord.randao_commitment = b'\xff'*32
    vrecord.balance = 18446744073709551615
    vrecord.start_dynasty = 18446744073709551615
    vrecord.end_dynasty = 18446744073709551615


  for i in range(0, 1000):
    shard_comittee_array = crystallized_state.indices_for_heights.add()
    for i in range(0, 10):
      scr = shard_comittee_array.array_shard_and_committee.add()
      scr.shard_id = 18446744073709551615
      for i in range(0, 1000):
        scr.committee.append(4294967295)


  attestation_record_bytes = attestation_record.SerializeToString()
  block_bytes = block.SerializeToString()
  shard_and_committee_bytes = shard_and_committee.SerializeToString()
  crosslink_record_bytes = crosslink_record.SerializeToString()
  validator_record_bytes = validator_record.SerializeToString()
  crystallized_state_bytes =  crystallized_state.SerializeToString()

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


def explain_max_packed():

  # Size of struct with only defaults
  attestation_record = packedmessages_pb2.PackedAttestationRecord()
  attestation_record.slot = 18446744073709551615
  attestation_record.shard_id = 18446744073709551615
  attestation_record.shard_block_hash = b'\xff'*32
  attestation_record.attester_bitfield = b'\xff'*32
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)
  attestation_record.aggregate_sig.append(18446744073709551615)

  block = packedmessages_pb2.PackedBlock()
  block.parent_hash= b'\xff'*32
  block.slot_number= 18446744073709551615
  block.randao_reveal= b'\xff'
  block.pow_chain_ref = b'\xff'*32
  block.active_state_hash = b'\xff'*32
  block.crystallized_state_root = b'\xff'*32

  shard_and_committee = packedmessages_pb2.PackedShardAndCommittee()
  shard_and_committee.shard_id = 18446744073709551615
  for i in range(0, 1000):
    shard_and_committee.committee.append(4294967295)

  crosslink_record = packedmessages_pb2.PackedCrosslinkRecord()
  crosslink_record.dynasty = 18446744073709551615
  crosslink_record.blockhash = b'\xff'*32

  validator_record = packedmessages_pb2.PackedValidatorRecord()
  validator_record.public_key = 18446744073709551615
  validator_record.withdrawal_shard = 18446744073709551615
  validator_record.withdrawal_address = b'\xff'*32
  validator_record.randao_commitment = b'\xff'*32
  validator_record.balance = 18446744073709551615
  validator_record.start_dynasty = 18446744073709551615
  validator_record.end_dynasty = 18446744073709551615

  crystallized_state = packedmessages_pb2.PackedCrystallizedState()
  crystallized_state.last_state_recalc = 18446744073709551615
  crystallized_state.justified_streak = 18446744073709551615
  crystallized_state.last_justified_slot = 18446744073709551615
  crystallized_state.last_finalized_slot = 18446744073709551615
  crystallized_state.current_dynasty = 18446744073709551615
  crystallized_state.crosslinking_start_shard = 18446744073709551615
  crystallized_state.total_deposits = 18446744073709551615
  crystallized_state.dynasty_seed = b'\xff'*32
  crystallized_state.dynasty_seed_last_reset = 18446744073709551615


  for i in range(0, 1000):
    crecord = crystallized_state.crosslink_records.add()
    crecord.dynasty = 18446744073709551615
    crecord.blockhash = b'\xff'*32

  for i in range(0, 1000):
    vrecord = crystallized_state.validators.add()
    vrecord.public_key = 18446744073709551615
    vrecord.withdrawal_shard = 18446744073709551615
    vrecord.withdrawal_address = b'\xff'*32
    vrecord.randao_commitment = b'\xff'*32
    vrecord.balance = 18446744073709551615
    vrecord.start_dynasty = 18446744073709551615
    vrecord.end_dynasty = 18446744073709551615


  for i in range(0, 1000):
    shard_comittee_array = crystallized_state.indices_for_heights.add()
    for i in range(0, 10):
      scr = shard_comittee_array.array_shard_and_committee.add()
      scr.shard_id = 18446744073709551615
      for i in range(0, 1000):
        scr.committee.append(4294967295)


  attestation_record_bytes = attestation_record.SerializeToString()
  block_bytes = block.SerializeToString()
  shard_and_committee_bytes = shard_and_committee.SerializeToString()
  crosslink_record_bytes = crosslink_record.SerializeToString()
  validator_record_bytes = validator_record.SerializeToString()
  crystallized_state_bytes =  crystallized_state.SerializeToString()

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
  parser = argparse.ArgumentParser(description='Testing Cap\'n Proto')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
      help='Verbose (Show all prints)')
  args = parser.parse_args()
  verbose = args.verbose

  results = []
  results.append(explain_default_size())
  results.append(explain_default_packed())
  results.append(explain_max_size())
  results.append(explain_max_packed())

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


