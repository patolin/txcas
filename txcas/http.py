

# Standard library
import cgi
import base64
from StringIO import StringIO
from urllib import urlencode
import urlparse

# External modules
from treq import content, text_content, json_content

from twisted.web.client import Agent, FileBodyProducer, readBody
from twisted.internet import reactor
from twisted.internet.ssl import ClientContextFactory

class WebClientContextFactory(ClientContextFactory):
    """
    Context factory does *not* verify SSL cert.
    """
    def getContext(self, hostname, port):
        return ClientContextFactory.getContext(self)

def request(method, url, headers=None, params=None, data=None, auth=None):
    p = urlparse.urlparse(url)
    if p.scheme.lower() == 'https':
        contextFactory = WebClientContextFactory()
    else:
        contextFactory = None
    body = None
    if data is not None:
        body = FileBodyProducer(StringIO(data))
    if params is not None:
        if p.params == '':
            param_str = urlencode(params)
        else:
            param_str = p.params + '&' + urlencode(params)
        p = urlparse.ParseResult(*tuple(p[:4] + (param_str,) + p[5:]))
        url = urlparse.urlunparse(p)

    if auth is not None:
        auth = "%s:%s" % auth
        b64auth = base64.b64encode(auth)
        auth = 'Basic %s' % b64auth
        if headers is None:
            headers = Headers({'Authorization': [auth]})
        else:
            if not headers.hasHeader('Authorization'):
                headers.addRawHeader('Authorization', auth)

    agent = Agent(reactor, contextFactory)
    d = agent.request(
        method, 
        url,
        headers=headers,
        bodyProducer=body)
    return d

def post(*args, **kwds):
    return request('POST', *args, **kwds)

def get(*args, **kwds):
    return request('GET', *args, **kwds)

def put(*args, **kwds):
    return request('PUT', *args, **kwds)

def delete(*args, **kwds):
    return request('DELETE', *args, **kwds)