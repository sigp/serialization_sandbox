#!/usr/bin/env python

import argparse
import texttable
import sys
import os
import time
import timeit

# Setting up paths
sys.path.append(os.path.join(sys.path[0], "beacon_chain"))
sys.path.append(os.path.join(sys.path[0], "cpnp"))
sys.path.append(os.path.join(sys.path[0], "fbuffers"))
sys.path.append(os.path.join(sys.path[0], "mpack"))
sys.path.append(os.path.join(sys.path[0], "pbuf"))
sys.path.append(os.path.join(sys.path[0], "pythonpickle"))
sys.path.append(os.path.join(sys.path[0], "smp"))
sys.path.append(os.path.join(sys.path[0], "rlpserialize"))

# Import our results
import cpnp
import fbuffers
import mpack
import pbuf
import pythonpickle
import smp
import rlpserialize

# Verbosity
verbose = False

# List of serializers
SERIALIZERS = {
    'Cap\'n Proto': cpnp,
    'Flatbuffers': fbuffers,
    'MsgPack': mpack,
    'Protobuf': pbuf,
    'Pickle': pythonpickle,
    'SimpleSerializer': smp,
    'RLP Serialize': rlpserialize,
}

# List of modules corresponding to serializer names
SERIALIZER_MODULES = {
    'Cap\'n Proto': 'cpnp',
    'Flatbuffers': 'fbuffers',
    'MsgPack': 'mpack',
    'Protobuf': 'pbuf',
    'Pickle': 'pythonpickel',
    'SimpleSerializer': 'smp',
    'RLP Serialize': 'rlpserialize',
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
            try:
                val = result_raw[res][item]
            except KeyError:
                val = "NA"
            row.append(val)
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


def get_size_results(args):
    """
    Get results of the experiments comparing message sizes.
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
    """
    Display the message size experiment results.
    """
    headers = list(SERIALIZERS.keys())
    rows = ['attestationRecord', 'block', 'shardAndCommittee',
            'crosslinkRecord', 'validatorRecord', 'crystallizedState']
    print_result_table('Message Size (bytes): Default Values', headers, rows, res['default'])
    print_result_table('Message Size (bytes): Max Values', headers, rows, res['max'])


def get_timing_results(args):
    """
    Get results of the experiments comparing running times.
    """
    # Initialize a dict with a key for each serializer
    results = dict((name, {}) for name in SERIALIZERS.keys())
    # Run through each serializer and get results
    for i in SERIALIZERS:
        """
        Get the benchmarking module for this serializer,
        read each method on the `Serializer_Bench()` class
        and run a timeit on each method that begins with
        "bench_".
        """
        try:
            bench_module = SERIALIZERS[i].bench
        except AttributeError:
            print("Skipping {}, no benchmarking module present.".format(i))
            continue
        bench_instance = bench_module.Serializer_Bench()
        method_list = [func for func in dir(bench_instance)
                       if callable(getattr(bench_instance, func))]
        for method in method_list:
            if method.startswith("bench_"):
                results[i][method] = execute_timeit(
                    module_name=SERIALIZER_MODULES[i],
                    method_name=method,
                    repeats=args.repeats,
                    loops=args.loops
                )
    return {
        "results": results,
        "repeats": args.repeats,
        "loops": args.loops,
    }


def execute_timeit(module_name, method_name, repeats, loops):
    method = "bench.{}()".format(method_name)
    setup = ("from {}.bench import Serializer_Bench;"
             "bench=Serializer_Bench()").format(module_name)
    results = timeit.repeat(
        method,
        setup=setup,
        repeat=repeats,
        timer=time.time,
        number=loops
    )
    return {
        "results": results,
        "average": (sum(results)/len(results))
    }


def display_timing_results(res):
    """
    Display the running time experiment results.
    """
    raw = res["results"]
    bench_names = []
    averages = dict((name, {}) for name in raw.keys())
    for (serializer_name, serializer) in raw.items():
        for (bench_name, bench_results) in serializer.items():
            bench_names.append(bench_name)
            averages[serializer_name][bench_name] = bench_results["average"]

    headers = list(SERIALIZERS.keys())
    rows = bench_names
    table_name = ("Timing Results (seconds):"
                  "averages over {} repeats, {} loops").format(
                      res["repeats"], res["loops"])
    print_result_table(table_name, headers, rows, averages)


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
        res = get_method(args)
        if(args.raw_output):
            print(res)
        else:
            display_method(res)


################################################################################
# Parse Arguments
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
parser.add_argument('-n', '--repeats', dest='repeats', default=10,
                    help="Number of timeit repeats (only for timing).")
parser.add_argument('-l', '--loops', dest='loops', default=1,
                    help="Number of timeit loops (only for timing).")
args = parser.parse_args()
verbose = args.verbose
main(args)
