
.PHONY : all

all : 6/i386.repo 6/x86_64.repo 7/i386.repo 7/x86_64.repo

%.repo :
	createrepo -s sha $*
	find . -type d |xargs chmod o+rx
	find . -type f |xargs chmod o+r
