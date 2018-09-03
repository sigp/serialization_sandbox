import rlp
from rlp.sedes import big_endian_int, CountableList


class ShardAndCommittee(rlp.Serializable):
    fields = [
        # The shard ID
        ('shard_id', big_endian_int),
        # Validator indices
        ('committee', CountableList(big_endian_int)),
    ]

    defaults = {
        'shard_id': 0,
        'committee': [],
    }

    def __init__(self, **kwargs):
        vargs = {}
        for k in list(self.defaults.keys()):
            assert k in kwargs or k in self.defaults
            vargs[k] = kwargs.get(k) if k in kwargs else self.defaults.get(k)
        super(ShardAndCommittee, self).__init__(**vargs)
