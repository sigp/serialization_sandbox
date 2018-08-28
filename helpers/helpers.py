#!/usr/bin/env python

###############################
# Constants
###############################
MAX_U64 = 18446744073709551615
MAX_U32 = 4294967295
MAX_U16 = 65535
MAX_I64 = int(((MAX_U64 + 1) / 2) - 1)
MAX_I32 = int(((MAX_U32 + 1) / 2) - 1)
MAX_I16 = int(((MAX_U16 + 1) / 2) - 1)
MAX_256 = 2**256 - 1
EMPTY_BYTES = b'\x00' * 32
MAX_BYTES = b'\xff' * 32
SINGLE_EMPTY = b'\x00'
SINGLE_MAX = b'\xff'
ADDRESS_BYTES = b'\xff' * 20

# TODO confirm numbers

MAX_VALIDATORS = 100000
MAX_ATTESTATIONS = 100000
PLACEHOLDER = 1000


def compare_messages(a, b):
    attr_a = [getattr(a, x) for x in a.fields if not x.startswith('__') and not callable(getattr(a, x))]
    attr_b = [getattr(b, x) for x in b.fields if not x.startswith('__') and not callable(getattr(b, x))]

    return (attr_a == attr_b)
