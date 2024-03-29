import argparse
import os
import os.path

from .. import database
from ..database.can.c_source import camel_to_snake_case, generate_ros2_msgs


def _do_generate_c_source_ros2_msgs(args):
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

    ros2_msgs = generate_ros2_msgs(
        dbase,
        database_name,
        args.bit_fields,
        )
    
    #ros2_msgs_cmake, ros2_msgs_pkgxml = generate_ros2_msgs_pkg_files(ros2_msgs, can_interface_pkg_name)
    
    os.makedirs(args.output_directory, exist_ok=True)

    for name_msg in ros2_msgs.keys():
        path_msg = os.path.join(args.output_directory, name_msg + '.msg')
        content_msg = ros2_msgs[name_msg]
        with open(path_msg, 'w') as fout:
            fout.write(content_msg)

    print(f'Successfully generated ROS2 messages.')


def add_subparser(subparsers):
    generate_c_source_parser = subparsers.add_parser(
        'generate_c_source_ros2_msgs',
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
        '-o', '--output-directory',
        default='.',
        help='Directory in which to write output files.')
    generate_c_source_parser.add_argument(
        'infile',
        help='Input database file.')
    generate_c_source_parser.set_defaults(func=_do_generate_c_source_ros2_msgs)
