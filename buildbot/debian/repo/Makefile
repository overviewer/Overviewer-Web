.PHONY : all clean Packages Sources

GENERATED_FILES=Release Release.bz2 Release.gz Release.gpg
GENERATED_FILES+=Packages Packages.bz2 Packages.gz
GENERATED_FILES+=Sources Sources.bz2 Sources.gz

all : ${GENERATED_FILES}

clean :
	rm -f ${GENERATED_FILES}

Release : Release.header Packages Packages.bz2 Packages.gz Sources Sources.bz2 Sources.gz
	./gen_hashes.py Packages* Sources* | cat Release.header - > Release

Release.gpg : Release
	rm -f Release.gpg
	gpg --use-agent --batch --no-tty --output Release.gpg -a --detach-sig Release < /dev/null
	chmod a+r Release.gpg

Packages :
	dpkg-scanpackages -m . /dev/null > Packages

Sources :
	dpkg-scansources . /dev/null > Sources

%.bz2 : %
	cat $< | bzip2 > $@

%.gz : %
	cat $< | gzip > $@
