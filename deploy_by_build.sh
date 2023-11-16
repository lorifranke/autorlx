#!/bin/bash

# Pull Docker dependencies
docker pull mysql

# Build AutoRL X Base
cd base                                 # Base image
docker build -t lorifranke/autorlx-base:0.1.0 .

# Build AutoRL X Server
cd ../server                            # Server image
docker build -t lorifranke/autorlx-server:0.1.0 .

# Build AutoRL X
cd ../ui                                # Interface image
docker build -t lorifranke/autorlx-ui:0.1.0 .

# Bring up the composition
cd ..
docker-compose up -d

# Visit AutoRL X in your browser
open http://localhost:3400