import sys
import uwsgi_proxy
import argparse

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='command')
subparsers.required = True

parser_curl = subparsers.add_parser('curl')

parser_curl.add_argument(
    'uwsgi_addr', nargs=1,
    help='Remote address of uWSGI server')

parser_curl.add_argument(
    'url', nargs='?', default='/',
    help='Url to uWSGI server, optionally contains hostname')


parser_server = subparsers.add_parser('server')

parser_server.add_argument(
    'uwsgi_addr', nargs=1,
    help='Remote address of uWSGI server')
parser_server.add_argument(
    '-n', '--http_host',
    help='HTTP_HOST header for uWSGI server')
parser_server.add_argument(
    '-l', '--local_addr', default='127.0.0.1',
    help='Local address of HTTP server')


def main(argv=sys.argv[1:]):
    if not argv:
        return parser.print_help()
    args = parser.parse_args(argv)
    print 'Params:', args.__dict__

    if args.command == 'curl':
        print uwsgi_proxy.client.curl(args.uwsgi_addr[0], args.url)

    if args.command == 'server':
        uwsgi_proxy.server.serve(
            uwsgi_addr=args.uwsgi_addr[0],
            uwsgi_host=args.http_host,
            local_addr=args.local_addr,
        )


# print(sys.argv[1:])
# uwsgi_proxy.server.serve(':8000', '10.130.230.237:3030', 'wms.sportamore.se')
# uwsgi_proxy.server.serve(sys, '10.130.230.237:3030', 'wms.sportamore.se')


if __name__ == '__main__':
    main()
