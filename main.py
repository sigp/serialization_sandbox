#!/usr/bin/env python

import argparse
import texttable
import sys
import os

# Setting up paths
sys.path.append(os.path.join(sys.path[0], "beacon_chain"))
sys.path.append(os.path.join(sys.path[0], "cpnp"))
sys.path.append(os.path.join(sys.path[0], "fbuffers"))
sys.path.append(os.path.join(sys.path[0], "mpack"))
sys.path.append(os.path.join(sys.path[0], "pbuf"))
sys.path.append(os.path.join(sys.path[0], "pythonpickle"))
sys.path.append(os.path.join(sys.path[0], "smp"))

# Import our results
import cpnp
import fbuffers
import mpack
import pbuf
import pythonpickle
import smp

# Verbosity
verbose = False

# List of serializers
SERIALIZERS = {
    'Cap\'n Proto': cpnp,
    'Flatbuffers': fbuffers,
    'MsgPack': mpack,
    'Protobuf': pbuf,
    'Pickle': pythonpickle,
    'SimpleSerializer': smp
}


def print_result_table(title, headers, row_keys, result_raw):
    """
    Prints the formatted table of results
    """
    table = texttable.Texttable()
    table.header(['Object'] + headers)
    table.set_cols_width([22] + [len(x) + 2 for x in SERIALIZERS])

    # Get row values from results
    for item in row_keys:
        row = [item]
        for res in result_raw:
            row.append(result_raw[res][item])
        table.add_row(tuple(row))
    out = table.draw()

    # Draw the title
    rowsize = len(out.split("\n")[0])
    mid = int((rowsize - (4 + len(title))) / 2)
    print("+{}+".format("-" * (rowsize - 2)))
    print("|{} {} {}|".format(
        " " * mid,                                      # Left spacing
        title,                                          # Title
        " " * (mid + (0 if rowsize % 2 == 0 else 1))      # Right Spacing
    ))

    # Print the table
    print(out)


def get_size_results():
    """
    Get results of the informative experiments.
    """
    results = {
        'default': {},
        'max': {},
    }

    # Run through each serializer and get results
    for i in SERIALIZERS:
        results['max'][i] = SERIALIZERS[i].info.explain_maxval_size()
        results['default'][i] = SERIALIZERS[i].info.explain_default_size()
        if(verbose):
            print(i)
            print(results['max'][i])
            print(results['default'][i])
    return results


def display_size_results(res):
    headers = list(SERIALIZERS.keys())
    rows = ['attestationRecord', 'block', 'shardAndCommittee',
            'crosslinkRecord', 'validatorRecord', 'crystallizedState']
    print_result_table('Info: Default Values', headers, rows, res['default'])
    print_result_table('Info: Max Values', headers, rows, res['max'])


def get_timing_results():
    raise NotImplementedError


def display_timing_results(res):
    raise NotImplementedError


def main(args):
    """
    Run the experiments based on user arguments.
    """
    if(not(args.no_info)):
        # Select methods for a given command
        if args.command == "message-size":
            get_method = get_size_results
            display_method = display_size_results
        elif args.command == "timing":
            get_method = get_timing_results
            display_method = display_timing_results

        # Get and display results
        res = get_method()
        if(args.raw_output):
            print(res)
        else:
            display_method(res)


################################################################################
# Parse Arguments
# TODO add other arguments as they are developed
################################################################################
parser = argparse.ArgumentParser(description='Testing Cap\'n Proto')
commands = (
    'message-size',
    'timing',
)
parser.add_argument('command', choices=commands,
                    help='Type of benchmarking to be performed')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help='Verbose (Show all prints)')
parser.add_argument('-ni', '--no-info', dest='no_info', action='store_true',
                    help='Hide Informative Stats')
parser.add_argument('-r', '--raw-output', dest='raw_output', action='store_true',
                    help="Raw output as object instead of table")
args = parser.parse_args()
verbose = args.verbose
main(args)
