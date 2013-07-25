# -*- coding: utf-8 -*-
"""
    vermin.wsgi
    ~~~~~~~~~~~

    This module implements some WSGI related helpers.

    :copyright: (c) 2013 by Philippe Ndiaye
    :license: MIT, see LICENSE for mor details.
"""
from urllib import quote


def get_request_method(environ):
    """Get the HTTP Request method used by the request."""
    method = environ.get('REQUEST_METHOD', u'get')
    return method


def get_content_length(environ):
    """Get the content length of the request."""
    content_length = environ.get('CONTENT_LENGTH', 0)
    return content_length


def get_script_name(environ):
    """Get the script name value of the request."""
    script_name = environ.get('SCRIPT_NAME', str('/'))
    return script_name


def get_path_info(environ):
    """Get the path info."""
    path_info = environ.get('PATH_INFO', str('/'))
    return path_info


def get_query_string(environ):
    """Get the query string."""
    query_string = environ.get('PATH_INFO', '')
    return query_string


def get_full_request_uri(environ):
    """Get the full request URI."""
    url = environ['wsgi.url_scheme'] + '://'
    if environ.get('HTTP_HOST'):
        url += environ.get('HTTP_HOST')
    else:
        url += environ['SERVER_NAME']

        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
                url += ':' + environ['SERVER_PORT']
        else:
            if environ['SERVER_PORT'] != '80':
                url += ':' + environ['SERVER_PORT']

    url += quote(environ.get('SCRIPT_NAME', ''))
    url += quote(environ.get('PATH_INFO', ''))
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']


def get_content_type(mimetype, charset):
    """Return the full content type string with charset for a mimetype.

    If the mimetype represents text, the charset is added as a charset
    parameter. Otherwise, the mimetype is returned unchanged.

    :param mimetype: the mimetype to be used as content type.
    :param charset: the charset to be appended if we deal with a
                    text mimetype.
    :return: the content type.
    """
    if (
        mimetype.startswith('text/') or
        mimetype == 'application/xml' or
        (mimetype.startswith('application/') and mimetype.endswith('+xml'))
    ):
        mimetype += '; charset=%s' % charset

    return mimetype
