# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Hello, World!: the simplest tipfy app.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
from tipfy import RequestHandler, Response
from tipfy.ext.jinja2 import render_response

import site


class HelloWorldHandler(RequestHandler):
    def get(self):
        
        
        return render_response('circle_loop.html', message='Hello, World!', site=site)


class PrettyHelloWorldHandler(RequestHandler):
    def get(self):
        """Simply returns a rendered template with an enigmatic salutation."""
        return render_response('hello_world.html', message='Hello, World!')
