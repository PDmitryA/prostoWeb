from cgi import parse_qsl

def application3(environ, start_response):
    output = 'Hello, world!\n'

    d = parse_qsl(environ['QUERY_STRING'])
    if environ['REQUEST_METHOD'] == 'POST':
        v = (environ['wsgi.input'].read().decode('ascii')).split("&")
        for ch in v:
        	output+= (ch + ' ')

    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            for ch in d:
                output+=(' = '.join(ch).join(' '))

    output_len = sum(len(line) for line in output)
    start_response('200 OK', [('Content-type', 'text/html'),
                              ('Content-Length', str(output_len))])
    return [output.encode('utf-8')]
