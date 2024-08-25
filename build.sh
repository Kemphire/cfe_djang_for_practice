#!/bin/bash

# select all the lines that doesn't start with # and pass it to xargs which will convert them into sutiable arguments for export and making then env variables
export $(grep -v '^#' .env | xargs -d '\n')

docker build \
	--build-arg DJANGO_SECRET_KEY="$DJANGO_SECRET_KEY" \
	--build-arg CONN_MAX_AGE="$CONN_MAX_AGE" \
	--build-arg DJANGO_DEBUG="$DJANGO_DEBUG" \
	--build-arg DATABASE_URL="$DATABASE_URL" \
	-t cfe-django .
