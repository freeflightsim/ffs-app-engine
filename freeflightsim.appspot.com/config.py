# -*- coding: utf-8 -*-
"""
    www site
    ~~~~~~

    :copyright: 2010 pete@freeflightsim.org
    :license: GPL
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
	
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
    ],
    
    # Enable the apps here
    'apps_installed': [
        'apps.www',
    ],
}
