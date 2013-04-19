#!/usr/bin/env python
import urllib2
import os
import sys
import git
from bs4 import BeautifulSoup

#Configuration
baseDir = '/home/user/strebel/continuousPerformanceEval/'
githubAtomFeed = 'https://github.com/uzh/signal-collect/commits/master.atom'
githubRepositories = ['git://github.com/uzh/signal-collect.git', 'git://github.com/uzh/signal-collect-graphs.git','git://github.com/uzh/signal-collect-evaluation.git']
lastCommitFile = baseDir + 'lastCommitId'
projectFolderNames = ['signal-collect', 'signal-collect-graphs', 'signal-collect-evaluation'] #last entry is assembled as jar
jarName = 'signal-collect-evaluation-assembly-2.1.0-SNAPSHOT.jar'

#cenerated attributes
executableFolderName = projectFolderNames[-1]
jarPath = baseDir + executableFolderName + "/target/" + jarName

#Test if spreadsheet parameters are supplied
if(len(sys.argv) < 3):
    print >> sys.stderr, "please provide your Google username (argv[1]) and password (argv[2]) as arguments"
    sys.exit(1)

#Find the latest version available on Github
usock = urllib2.urlopen(githubAtomFeed)
data = usock.read()
usock.close()

soup = BeautifulSoup(data)

latestCommit = soup.feed.entry.id.string.split("Commit/")[-1][:10]
latestCommitURL = soup.feed.entry.link['href']
latestCommitMsg = soup.feed.entry.title.string
latestCommitAuthor = soup.feed.entry.author.find().string

lastChecked = ""

#Read the latest locally built version
try:
   with open(lastCommitFile) as f:pass
   f = open(lastCommitFile, 'r')
   lastChecked = f.readline().strip()
   f.close()
except IOError as e:
   None
   
shouldRunEvaluation = False

#Download and build the latest commit if it hasn't been built before.
if(lastChecked!=latestCommit):
    print "----------------------------------"
    print "we have to check out a new version"
    print "=================================="
    print "commit:" + latestCommit
    print "see: " + latestCommitURL
    print "commit message: " + latestCommitMsg
    print "author: " + latestCommitAuthor
    print "----------------------------------"
    
    
    #remove project-folder if it exists
    for projectFolderName in projectFolderNames:
        os.system("cd "+ baseDir +"; rm -rdf " + projectFolderName)
    
    #check out the newest version from Github    
    for githubRepository in githubRepositories:
        git.Git().clone(githubRepository)

    
    print "started building jar"
    os.system("cd " + baseDir + executableFolderName + "; "+ baseDir+"sbt assembly;cd ..")
    print "done building jar"
    
    #copyJarToRoot = "cd "+ baseDir +"; cp " + executableFolderName + "/target/" + jarName + " ~"
    #os.system(copyJarToRoot)
    

    shouldRunEvaluation = True
    
elif(len(sys.argv) == 4 and sys.argv[3]=='debug'):
    shouldRunEvaluation = True

if(shouldRunEvaluation):
    #run some benchmarks
	
    args = sys.argv[1] 
    args += " " + sys.argv[2] 
    args += " " + jarPath 
    args += " " + latestCommit
    args += " " + latestCommitURL

    cmd = "java -cp " + jarPath + " com.signalcollect.evaluation.continuousperformance.SingleNodePageRank " + args 
    print cmd
    os.system(cmd)
    
    #set last commit file
    f = open(lastCommitFile, 'w')
    f.write(latestCommit)
    f.close
    
    
    
    
    

