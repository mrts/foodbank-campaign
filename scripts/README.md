# Remote server management with Fabric

Copy production DB:

```sh
export TOIDUPANK_SSH_HOST=user@example.org:22
fab -H $TOIDUPANK_SSH_HOST copyproddb
```

Deploy new version to test server:

```sh
export TOIDUPANK_SSH_HOST=user@example.org:22
fab -H $TOIDUPANK_SSH_HOST deploytest # or ./deploy-to-test.sh
```

Start a new campaign and download shift leaders:

```sh
cd new-campaign
fab -H $TOIDUPANK_SSH_HOST newcampaign \
    --old-start-date=2023-12-08 \
    --new-start-date=2024-04-12
```
