.PHONY : all clean Packages Sources

GENERATED_FILES=InRelease InRelease.gz InRelease.bz2 Release Release.bz2 Release.gz Release.gpg
GENERATED_FILES+=Packages Packages.bz2 Packages.gz
GENERATED_FILES+=Sources Sources.bz2 Sources.gz

all : ${GENERATED_FILES}

clean :
	rm -f ${GENERATED_FILES}

InRelease : Release
	rm -f InRelease
	gpg --batch -s --clearsign --digest-algo SHA512 --output InRelease -a Release < /dev/null
	chmod a+r InRelease

Release : Release.header main/binary-amd64/Packages main/binary-amd64/Packages.bz2 main/binary-amd64/Packages.gz main/source/Sources main/source/Sources.bz2 main/source/Sources.gz
	./gen_hashes.py main/binary-amd64/Packages* main/source/Sources* | cat Release.header - > Release

Release.gpg : Release
	rm -f Release.gpg
	gpg --batch --digest-algo SHA512 --output Release.gpg -a --detach-sig Release < /dev/null
	chmod a+r Release.gpg

main/binary-amd64/Packages :
	cd main/binary-amd64
	dpkg-scanpackages -m . /dev/null > main/binary-amd64/Packages
	cd ../..

main/source/Sources :
	cd main/source
	dpkg-scansources . /dev/null > main/source/Sources
	cd ../..

%.bz2 : %
	cat $< | bzip2 > $@

%.gz : %
	cat $< | gzip > $@
