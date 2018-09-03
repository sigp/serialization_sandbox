import rlp
from rlp.sedes import big_endian_int, binary, CountableList, List
from . import utils


class AttestationRecord(rlp.Serializable):
    """
    Attestation Record Class with RLP compatible fields
    """
    fields = [
        ('slot', big_endian_int),
        ('shard_id', big_endian_int),
        ('oblique_parent_hashes', CountableList(utils.hash32)),
        ('shard_block_hash', utils.hash32),
        ('attester_bitfield', binary),
        ('aggregate_sig', List([utils.int256, utils.int256]))
    ]

    defaults = {
        'slot': 0,
        'shard_id': 0,
        'oblique_parent_hashes': [],
        'shard_block_hash': b'\x00' * 32,
        'attester_bitfield': b'',
        'aggregate_sig': [0, 0],
    }

    def __init__(self, **kwargs):
        vargs = {}
        for k in list(self.defaults.keys()):
            assert k in kwargs or k in self.defaults
            vargs[k] = kwargs.get(k) if k in kwargs else self.defaults.get(k)
        super(AttestationRecord, self).__init__(**vargs)
