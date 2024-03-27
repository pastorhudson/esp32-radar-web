# FormationFLight Web Installer

This is an installer website for [FormationFLight](https://formationflight.org/).

[FormationFlight Latest Release](https://github.com/FormationFlight/FormationFlight/releases/latest)

[Visit installer website](https://flash.formationflight.com)

### Deployment

- This repo is setup for deploy on dokku/heroku style deploy
- You need to setup a persistant storage dir that maps to /app/storage and /app/www/storage
- On deploy it will run /scripts/update.py which downloads all the artifacts from the latest release and generates the appropriate manifest.json files for the esp-web tool.
- update.py is set to run hourly via cron job