import rlp
from rlp.sedes import big_endian_int, CountableList
from . import utils

from .crosslink_record import CrosslinkRecord
from .shard_and_committee import ShardAndCommittee
from .validator_record import ValidatorRecord


class CrystallizedState(rlp.Serializable):
    fields = [
        # List of validators
        ('validators', CountableList(ValidatorRecord)),
        # Last CrystallizedState recalculation
        ('last_state_recalc', big_endian_int),
        ('indices_for_heights', CountableList(CountableList(ShardAndCommittee))),
        # The last justified slot
        ('last_justified_slot', big_endian_int),
        # Number of consecutive justified slots ending at this one
        ('justified_streak', big_endian_int),
        # The last finalized slot
        ('last_finalized_slot', big_endian_int),
        # The current dynasty
        ('current_dynasty', big_endian_int),
        # The next shard that crosslinking assignment will start from
        ('crosslinking_start_shard', big_endian_int),
        # Records about the most recent crosslink for each shard
        ('crosslink_records', CountableList(CrosslinkRecord)),
        # Total balance of deposits
        ('total_deposits', utils.int256),
        # Used to select the committees for each shard
        ('dynasty_seed', utils.hash32),
        # Last epoch the crosslink seed was reset
        ('dynasty_seed_last_reset', big_endian_int),
    ]
    defaults = {
        'validators': [],
        'last_state_recalc': 0,
        'indices_for_heights': [],
        'last_justified_slot': 0,
        'justified_streak': 0,
        'last_finalized_slot': 0,
        'current_dynasty': 0,
        'crosslinking_start_shard': 0,
        'crosslink_records': [],
        'total_deposits': 0,
        'dynasty_seed': b'\x00' * 32,
        'dynasty_seed_last_reset': 0,
    }

    def __init__(self, **kwargs):
        vargs = {}
        for k in list(self.defaults.keys()):
            assert k in kwargs or k in self.defaults
            vargs[k] = kwargs.get(k) if k in kwargs else self.defaults.get(k)
        super(CrystallizedState, self).__init__(**vargs)
