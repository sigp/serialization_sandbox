import rlp
from rlp.sedes import big_endian_int
from . import utils


class ValidatorRecord(rlp.Serializable):
    fields = [
        # The validator's public key
        ('pubkey', utils.int256),
        # What shard the validator's balance will be sent to after withdrawal
        ('withdrawal_shard', big_endian_int),
        # And what address
        ('withdrawal_address', utils.address),
        # The validator's current RANDAO beacon commitment
        ('randao_commitment', utils.hash32),
        # Current balance
        ('balance', big_endian_int),
        # Dynasty where the validator is inducted
        ('start_dynasty', big_endian_int),
        # Dynasty where the validator leaves
        ('end_dynasty', big_endian_int),
    ]

    defaults = {
        'pubkey': 0,
        'withdrawal_shard': 0,
        'withdrawal_address': b'\x00' * 20,
        # The validator's current RANDAO beacon commitment
        'randao_commitment': b'\x00' * 30,
        # Current balance
        'balance': 0,
        # Dynasty where the validator is inducted
        'start_dynasty': 0,
        # Dynasty where the validator leaves
        'end_dynasty': 0,
    }

    def __init__(self, **kwargs):
        vargs = {}
        for k in list(self.defaults.keys()):
            assert k in kwargs or k in self.defaults
            vargs[k] = kwargs.get(k) if k in kwargs else self.defaults.get(k)
        super(ValidatorRecord, self).__init__(**vargs)
