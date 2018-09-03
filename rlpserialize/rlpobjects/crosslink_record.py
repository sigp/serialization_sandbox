import rlp
from rlp.sedes import big_endian_int
from . import utils


class CrosslinkRecord(rlp.Serializable):
    fields = [
        # What dynasty the crosslink was submitted in
        ('dynasty', big_endian_int),
        # The block hash
        ('hash', utils.hash32),
    ]
    defaults = {
        'dynasty': 0,
        'hash': b'\x00' * 32
    }

    def __init__(self, **kwargs):
        vargs = {}
        for k in list(self.defaults.keys()):
            assert k in kwargs or k in self.defaults
            vargs[k] = kwargs.get(k) if k in kwargs else self.defaults.get(k)
        super(CrosslinkRecord, self).__init__(**vargs)
