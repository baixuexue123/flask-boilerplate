#!/usr/bin/env bash

cat ./logs/gunicorn.pid | xargs kill -2
