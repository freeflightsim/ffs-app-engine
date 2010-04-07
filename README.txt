

// Setup local area/repos with git (git svn combination)
mkdir ffs
git svn init http://m2.daffodil.uk.com/svn/ffs
user=willie


// Fetch the latest version from HEAD
git svn fetch


// make changes locally merge etc
git add foo.txt
git commit -a -m "My commit message"

// Commit changes to HEAD
git svn dcommit

