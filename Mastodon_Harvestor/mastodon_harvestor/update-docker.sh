#!/usr/bin/env bash
docker build -t mastodon-harvestor .
docker tag mastodon-harvestor djang9303/mastodon-harvestor:1.5
docker login
docker push djang9303/mastodon-harvestor:1.5
docker logout
