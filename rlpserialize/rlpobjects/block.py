import rlp
from rlp.sedes import big_endian_int, binary, CountableList, List
from . import utils

from .attestation_record import AttestationRecord

class Block(rlp.Serializable):
    """
    Block message with RLP compatible fields
    """

    fields = [
        ('parent_hash', utils.hash32),
        ('slot_number', big_endian_int),
        ('randao_reveal', utils.hash32),
        ('attestations', CountableList(AttestationRecord)),
        ('pow_chain_ref', utils.hash32),
        ('active_state_root', utils.hash32),
        ('crystallized_state_root', utils.hash32)
    ]

    defaults = {
        'parent_hash': b'\x00' * 32,
        'slot_number': 0,
        'randao_reveal': b'\x00' * 32,
        'attestations': [],
        'pow_chain_ref': b'\x00' * 32,
        'active_state_root': b'\x00' * 32,
        'crystallized_state_root': b'\x00' * 32,
    }

    def __init__(self, **kwargs):
        vargs = {}
        for k in list(self.defaults.keys()):
            assert k in kwargs or k in self.defaults
            vargs[k] = kwargs.get(k) if k in kwargs else self.defaults.get(k)
        super(Block, self).__init__(**vargs)
