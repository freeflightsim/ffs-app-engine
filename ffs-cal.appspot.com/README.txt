===================================================
===  freeflightsim.appspot.com ===
===================================================


This is the main front end domain

Main code is dJango templating

conf.py - main configuration
main.py - the main script that runs
slideshow.py - the script that runs for the slide show

app/ - main application code
atom/ - atom api module and needs to be at this location
gdata/ - google data api 
images/ - static images
js/ - javascript (libs to be on ffs-cache as CDN)
static/ - various static files eg robots.txt
style_sheets/ - css
templates/ - all the html
    MAIN.html - main "container" for pages
    pages/ - the individual html pages
    SLIDE_SHOW.html - the slide show container
    slideshows/ - directory containing the html slides

