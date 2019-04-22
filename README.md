# Overviewer Web

Source for https://overviewer.org:

- [Flask](http://flask.pocoo.org/) web app
- [Buildbot](https://buildbot.net/)

## Confidential Files

Place an ASCII-armored private GPG key dump in `buildbot/codesign.asc` e.g.:

```bash
$ gpg --export-secret-key YOUR_EMAIL_HERE > codesign.asc
```

Create a `confidential.env` file using `confidential.env.example` as an example.

Once those are in place, you can rebuild the images and bring
everything online with:

    docker-compose build
    docker-compose up -d

## Local Development

Add `ENV=dev` to `confidential.env`. This will **disable EC2 builders** and configure Buildbot to use local resources (i.e. localhost URLs).
- AWS `confidential.env` settings will be ignored

Further `confidential.env` settings available (not applicable in production environment):

- `DEFAULT_REPOSITORY` - Set the GitHub repo for Minecraft-Overviewer, useful if you wish to test the builders using a fork of https://github.com/overviewer/Minecraft-Overviewer
- `DISABLE_GITHUB_AUTH` - Disable GitHub authentication. Buildbot is locked down to only allow members of the Overviewer [organisation](https://github.com/overviewer) to start/configure builds, passing this setting will allow unauthenticated access.
  - N.B this setting acts as a flag: it's presence indicates `True`, the actual value does not matter
