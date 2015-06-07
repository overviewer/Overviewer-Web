
.PHONY : all

all : 5/i386.repo 5/x86_64.repo 6/i386.repo 6/x86_64.repo 16/i386.repo 16/x86_64.repo

%.repo :
	createrepo -s sha $*
	find . -type d |xargs chmod o+rx
	find . -type f |xargs chmod o+r
