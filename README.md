First some confidential files need making. Copy over and modify the
following example files:

 * confidential.env.example

You will also need to place an ASCII-armored private GPG key dump in:

 * buildbot/codesign.asc

Once those are in place, you can rebuild the images and bring
everything online with:

    docker-compose build
    docker-compose up -d
