=============================================================
== App Engine - freeflightsim.appsot.com ==
=============================================================

== Dev server ==
Execute 
./run_server 
to start the local server, browse at
http://localhost:8080/

== App Update ==
Update the online application with
./upload.sh

### Important ###
If you need to bump the version number in app.yaml,
then increment as digits eg "1,2,3,4" etc
DO NOT USE "2.dev" or any non mumeric characters.
The manual says you can, but experience shows is causes problems.



=============================================================
== Git Svn ==
=============================================================
//** This is a conundrum
//* you wont see this document unless u checked out ;-) 

//*  Setup local area/repos with git (git svn combination)
mkdir ffs
git svn init http://m2.daffodil.uk.com/svn/ffs
user=willie


//* Fetch the latest version from HEAD
git svn fetch

//* Recommend to create branch so "master" always reflect svn
git branch newstuff
git checkout newstuff

//* make changes
git add foo.txt
git commit -a -m "My commit message"

//* now get ready to commit to svn by switching to "master"
git checkout master
git svn fetch  // get any changes from svn
git merge newstuff // merge in the changes
git svn dcommit // push changes to svn


