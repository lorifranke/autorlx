#!/bin/bash

# Pull Docker dependencies
docker pull mysql
docker pull lorifranke/autorlx-server:0.1.0
docker pull lorifranke/autorlx-ui:0.1.0

# Bring up the composition
cd ..
docker-compose up -d

# Visit AutoRL X in your browser
open http://localhost:3400