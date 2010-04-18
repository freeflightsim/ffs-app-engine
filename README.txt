
 _____                  _____  _  _         _      _    ____   _            
|  ___|_ __  ___   ___ |  ___|| |(_)  __ _ | |__  | |_ / ___| (_) _ __ ___  
| |_  | '__|/ _ \ / _ \| |_   | || | / _` || '_ \ | __|\___ \ | || '_ ` _ \ 
|  _| | |  |  __/|  __/|  _|  | || || (_| || | | || |_  ___) || || | | | | |
|_|   |_|   \___| \___||_|    |_||_| \__, ||_| |_| \__||____/ |_||_| |_| |_|
                                     |___/       
                           
----------------------------------------------------------------------------
    ---  App Engine Powered Sites - http://freeflightsim.org      ---
-----------------------------------------------------------------------------


This respository contains the latest gae websites, and includes the dev sdk.

Project at - http://code.google.com/p/freeflightsim/
Code at - http://github.com/FreeFlightSim


===============================================================================
== Development  ==
===============================================================================
The GAE currently used python 2.5. There should be minor problem with running
on 2.5+, notable exception is 
> import simplejson as json # python 2.5
> import json # python 2.6+ json is built 
> from django.utils import simplejson as json << Gae Workaround

"_site_/" below is one of the domain subdirectories eg freeflightsim.appsot.com
To run a local development server:-

# goto some directory
cd ~

# take a clone from github, this will create a ffs-app-engine sub dir
git clone git@github.com:FreeFlightSim/ffs-app-engine.git

# run a site on the dev server 
python ./gae/dev_appserver.py _site_/

# then browse at
http://localhost:8080/

## Update the online app
python ./gae/appcfg.py _site_/
>>  enter login details


==============================================================
=== Important ===
==============================================================
If you need to bump the version number in app.yaml,
then increment as digits eg "1,2,3,4" etc
DO NOT USE "2.dev" or any non mumeric characters.
The manual says you can, but experience shows is causes problems.

ALSO
If you bump the version, you will need to change the "default"
application to newest in the control panel.




