import argparse
import os
import os.path

from .. import database
from ..database.can.c_source import camel_to_snake_case, generate_transceiver


def _do_generate_c_source_endec(args):
    dbase = database.load_file(args.infile,
                               encoding=args.encoding,
                               prune_choices=args.prune,
                               strict=not args.no_strict)

    if args.database_name is None:
        basename = os.path.basename(args.infile)
        database_name = os.path.splitext(basename)[0]
        database_name = camel_to_snake_case(database_name)
    else:
        database_name = args.database_name
        
    filename_endec_hpp = 'endec.hpp'

    endec_hpp, transceiver_h, transceiver_cpp = generate_transceiver(
        dbase,
        database_name,
        args.bit_fields
        )
        
    os.makedirs(args.output_headers, exist_ok=True)
    os.makedirs(args.output_sources, exist_ok=True)

    path_msg = os.path.join(args.output_headers, filename_endec_hpp)
    with open(path_msg, 'w') as fout:
        fout.write(endec_hpp)
        
    print(f'')
    print(f'Generated CAN endec Library based on ' + args.infile)
    print(f'')
    print(f'Headers:')
    print(f'\t' + os.path.join(os.getcwd(), args.output_headers, filename_endec_hpp))





def add_subparser(subparsers):
    generate_c_source_parser = subparsers.add_parser(
        'generate_c_source_endec',
        description='Generate C source code from given database file.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    generate_c_source_parser.add_argument(
        '--database-name',
        help=('The database name.  Uses the stem of the input file name if not'
              ' specified.'))
    generate_c_source_parser.add_argument(
        '--bit-fields',
        action='store_true',
        help='Use bit fields to minimize struct sizes.')
    generate_c_source_parser.add_argument(
        '-e', '--encoding',
        help='File encoding.')
    generate_c_source_parser.add_argument(
        '--prune',
        action='store_true',
        help='Try to shorten the names of named signal choices.')
    generate_c_source_parser.add_argument(
        '--no-strict',
        action='store_true',
        help='Skip database consistency checks.')
    generate_c_source_parser.add_argument(
        '--output-headers',
        default='.',
        help='Relative directory in which to write output header files.')
    generate_c_source_parser.add_argument(
        '--output-sources',
        default='.',
        help='Realtive directory in which to write output source files.')
    generate_c_source_parser.add_argument(
        'infile',
        help='Input database file.')
    generate_c_source_parser.set_defaults(func=_do_generate_c_source_endec)
