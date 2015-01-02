from __future__ import print_function, unicode_literals
import argparse
import sys
from .core import Togu, IncompleteEnvironmentException

def main(arguments=None):
    parser = argparse.ArgumentParser(description='ping shinken service '
                                     'in supervisord')
    parser.add_argument('--port', '-p', metavar='PORT', type=int,
                        required=True,
                        help='port of the shinken daemon to check')
    parser.add_argument('--service-name', '-n', metavar='SERVICE', type=str,
                        required=True,
                        help='name of the service in supervisord')
    parser.add_argument('--retry', '-r', metavar='TIMES', type=int, default=3,
                        help='number of times to retry before restarting')
    parser.add_argument('--timeout', '-t', metavar='TIMES', type=int,
                        default=10, help='time to respond to ping')
    args = parser.parse_args(arguments)

    try:
        Togu(args.port, args.service_name, args.timeout, args.retry).run()
    except IncompleteEnvironmentException as exc:
        sys.exit('this program must be run as an [eventlistener] under '
                 'supervisor\nmissing environment variable: {0}'.format(exc))
