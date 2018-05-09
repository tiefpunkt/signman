# SignMan server
```
git clone https://github.com/tiefpunkt/signman.git
docker build -t "tiefpunkt/signman" server

docker run -d \
  --name signman \
  -v /srv/signman:/data:rw \
  -e VIRTUAL_HOST=signman,signman.intern.munichmakerlab.de \
  tiefpunkt/signman
```

## Updating
To update existing databases to the latest schema version, execute **"migrate.py"**. 