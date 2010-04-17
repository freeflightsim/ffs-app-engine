
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


=============================================================================
== Development Server
=============================================================================
To run a local development server:-

# goto some directory
cd ~

# take a clone from github, this will create a ffs-app-engine sub dir
git clone git@github.com:FreeFlightSim/ffs-app-engine.git

# then make the shell scripts executable
cd ffs-app-engine
chmod +x *.sh

# run the dev server
./run_server 

# then browse to
http://localhost:8080/

## Update the online app
./upload.sh
# << then enter login details



===# Important #===
If you need to bump the version number in app.yaml,
then increment as digits eg "1,2,3,4" etc
DO NOT USE "2.dev" or any non mumeric characters.
The manual says you can, but experience shows is causes problems.


