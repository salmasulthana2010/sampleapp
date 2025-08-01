#!/bin/bash

BRANCH=$1
DEPLOY_DIR="/home/ec2-user/${BRANCH}_site"

echo "Deploying branch: $BRANCH to $DEPLOY_DIR"
cd $DEPLOY_DIR || exit 1

# Create a deploy log
echo "Deployed from branch $BRANCH at $(date)" > deployed.log

# Optional: Restart service, move files, etc.
echo "Deployment complete."
