# uwsgi tools


### uwsgi_curl

Usage:

```
$ uwsgi_curl -h
usage: uwsgi_curl [-h] uwsgi_addr [url]

positional arguments:
  uwsgi_addr  Remote address of uWSGI server
  url         Request URI optionally containing hostname

optional arguments:
  -h, --help  show this help message and exit
```

Example:

```
$ uwsgi_curl 10.0.0.1:3030 host.name/login

$ uwsgi_curl 10.0.0.1 host.name

$ uwsgi_curl 10.0.0.1 /login

$ uwsgi_curl 10.0.0.1
```


### uwsgi_proxy

Usage:

```
$ uwsgi_proxy -h
usage: uwsgi_proxy [-h] [-n HTTP_HOST] [-l LOCAL_ADDR] [-s] uwsgi_addr

positional arguments:
  uwsgi_addr            Remote address of uWSGI server

optional arguments:
  -h, --help            show this help message and exit
  -n HTTP_HOST, --http-host HTTP_HOST
                        HTTP_HOST header for uWSGI server
  -l LOCAL_ADDR, --local-addr LOCAL_ADDR
                        Local address of HTTP server
  -s, --redirect-static
                        Redirect static requests to host
```

Example:

```
$ uwsgi_proxy -s -n host.name 10.0.0.1
Proxying remote uWSGI server 10.0.0.1:3030 "host.name" to local HTTP server 127.0.0.1:3030...
127.0.0.1 - - [01/Oct/2015 15:25:50] GET /wrong-uri
HTTP/1.1 404 NOT FOUND
X-Frame-Options: SAMEORIGIN
Content-Type: text/html
75
```
