#!/bin/bash

cd server && go build init.go && cd .. && cd client && go build init.go