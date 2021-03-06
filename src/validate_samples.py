#!/usr/bin/env python3

import argparse
import sys
import inspect

from ingest_validation_tools.error_report import ErrorReport
from ingest_validation_tools.samples import Samples
from ingest_validation_tools.argparse_types import ShowUsageException


def make_parser():
    parser = argparse.ArgumentParser(
        description='Validate a HuBMAP Sample metadata TSV.')
    parser.add_argument(
        '--path', required=True,
        help='Sample metadata.tsv path. ')
    error_report_methods = [
        name for (name, type) in inspect.getmembers(ErrorReport)
        if name.startswith('as_')
    ]
    parser.add_argument('--output', choices=error_report_methods,
                        default='as_text')
    return parser


# We want the error handling inside the __name__ == '__main__' section
# to be able to show the usage string if it catches a ShowUsageException.
# Defining this at the top level makes that possible.
parser = make_parser()


def main():
    args = parser.parse_args()
    sample_args = {
        'path': args.path
    }

    samples = Samples(**sample_args)
    errors = samples.get_errors()
    report = ErrorReport(errors)
    print(getattr(report, args.output)())
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        exit_status = main()
    except ShowUsageException as e:
        print(parser.format_usage(), file=sys.stderr)
        print(e, file=sys.stderr)
        exit_status = 2
    sys.exit(exit_status)
