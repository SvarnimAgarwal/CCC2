# Mastodon Harvestor User Guide

The commands below demonstate how the docker images can be used to launch container using terminal. For MRC instance, there are ansible scripts that had been automated.

The docker images for mastodon harvestor is available in the following link:
- https://hub.docker.com/repository/docker/djang9303/mastodon-harvestor/general

### Run Docker Container
'''console
foo@bar:~$ docker run -d --network=host \
    -e MASTODON_ACCESS_TOKEN_SOCIAL="token detail" \
    -e MASTODON_ACCESS_TOKEN_AU="token detail" \
    -e MASTODON_ACCESS_TOKEN_CLOUD="token detail"  \
    -e MASTODON_ACCESS_TOKEN_WORLD="token detail" \
    -e MASTODON_ACCESS_TOKEN_UK="token detail" \
    -e DB_URL="url to database" \
    -e DB_USERNAME="username of database" \
    -e DB_PASSWORD="password of database" \
    djang9303@mastodon-harvestor:1.5
'''

The container requires token details and db details to be set as envrionmental variable. The status of the token also should be available in the database in order to be used.

### Checking Container Logs
'''console
foo@bar:~$ docker logs "container id"
'''

The logs are available some time after the container is launched

### Run Docker Service
Create Docker Swarm
'''console
foo@bar:~$ docker swarm init
'''

Run Docker Service
'''console
foo@bar:~$ docker service create \
    --name mastodon-harvestor \
    --publish published=5984,target=5984 \
    --replica 3 \
    --env MASTODON_ACCESS_TOKEN_SOCIAL="token detail" \
    --env MASTODON_ACCESS_TOKEN_AU="token detail" \
    --env MASTODON_ACCESS_TOKEN_CLOUD="token detail"  \
    --env MASTODON_ACCESS_TOKEN_WORLD="token detail" \
    --env MASTODON_ACCESS_TOKEN_UK="token detail" \
    --env DB_URL="url to database" \
    --env DB_USERNAME="username of database" \
    --env DB_PASSWORD="password of database" \
    djang9303@mastodon-harvestor:1.5
'''