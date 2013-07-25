# -*- coding: utf-8 -*-
"""
    vermin.wrappers
    ~~~~~~~~~~~~~~~

    The wrappers are just some request/response objects performing what a
    user would see when he types "http://google.com" in this browser.
    The Request object contains the informations sent to the server, and the
    Response object represents the response sent back to the client.

    Both are handled by the Requests librairy.

    :copyright: (c) 2013 by Philippe Ndiaye
    :license: MIT, see LICENSE for mor details.

"""
from vermin.wsgi import (get_request_method, get_content_length,
                         get_path_info, get_query_string,
                         get_full_request_uri, get_content_type)
from vermin.utils import integer_types, text_type
from vermin.http import HTTP_STATUSES


class Request(object):
    """Basic request object created with the WSGI environment as
    first argument. It will add itself to the WSGI environment as
    ``'vermin.request`` for debugging purposes.
    """

    #: the default charset used for the request
    default_charset = 'utf-8'

    def __init__(self, environ):
        self.environ = environ
        self.method = get_request_method(environ)
        self.content_length = get_content_length(environ)
        self.path_info = get_path_info(environ)
        self.query_string = get_query_string(environ)
        self.request_uri = get_full_request_uri(environ)


class Response(object):
    """The Response object."""

    #: the default charset used in the response
    default_charset = 'utf-8'

    #: the default mimetype used in the response
    default_mimetype = 'text/plain'

    #: the default http status code
    default_status = 200

    def __init__(self,
                 response=None,
                 status=None,
                 headers=None,
                 mimetype=None,
                 content_type=None):

        if headers is None:
            self.headers = []
        if headers is not None:
            self.headers = headers

        if content_type is None:
            if mimetype is None and 'content-type' not in self.headers:
                mimetype = self.default_mimetype
            if mimetype is not None:
                mimetype = get_content_type(mimetype, self.default_charset)
            content_type = mimetype
        if content_type is not None:
            self.headers.append(('CONTENT_TYPE', content_type))

        if status is None:
            status = self.default_status
        if isinstance(status, integer_types):
            self.status_code = status
        else:
            self.status = status

        # the response is set last so that the data are always
        # set with the correct charset.
        if response is None:
            self.response = []
        elif isinstance(response, (text_type, bytes, bytearray)):
            self.set_data(response)
        else:
            self.response = response

    def set_data(self, data):
        """Sets a string as response. The data to be set must a
        unicode or bytestring. The value is automatically encoded
        to the response charset or the default one (utf-8) if it is
        a unicode string.
        """
        # the Content-Length WSGI environ variable is automatically
        # set to the length of the data (encoded or unchanged)
        if isinstance(data, text_type):
            data = data.encode(self.default_charset)
        else:
            data = bytes(data)

        self.response = [data]
        content_length = ('Content-Length', str(len(data)))
        self.headers.append(content_length)

    def get_wsgi_headers(self):
        return self.headers

    def get_wsgi_response(self):
        headers = self.get_wsgi_headers()
        response = self.response
        return headers, response

    def __call__(self, environ, start_response):
        response_headers, response = self.get_wsgi_response()
        status = '%s %s' % (self.status_code,
                            HTTP_STATUSES[self.status_code])
        start_response(status, response_headers)
        return self.response
