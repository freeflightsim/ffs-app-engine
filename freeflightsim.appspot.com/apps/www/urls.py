# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule


def get_rules(app):
    """Returns a list of URL rules for the Hello, World! application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        Rule('/', endpoint='hello-world', handler='apps.www.handlers.HelloWorldHandler'),
        Rule('/pretty', endpoint='hello-world-pretty', handler='apps.www.handlers.PrettyHelloWorldHandler'),
    ]

    return rules
