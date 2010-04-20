===================================================
===  login.freeflightsim.org - ffs-login.appspot.com ===
===================================================

Authentication central.

Idea is that this will be the master machine for login

The Selector is from:
http://code.google.com/p/openid-selector



Copy conf.skel.py to conf.py for production
conf.py - main configuration

main.py - the main script that runs


app/ - main application code

images/ - static images
js/ - javascript (libs to be on ffs-cache as CDN)
static/ - various static files eg robots.txt
style_sheets/ - css
templates/ - all the html
    MAIN.html - main "container" for pages
    pages/ - the individual html pages

