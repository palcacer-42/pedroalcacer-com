#!/bin/bash

echo "Building the project..."
# Build the project.
hugo # if using a theme, replace with `hugo -t <YOURTHEME>`

echo "Navigating to the public directory..."
# Go To Public folder
cd public

echo "Adding changes to git..."
# Add changes to git.
git add .

echo "Committing changes..."
# Commit changes.
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

echo "Pushing to gh-pages branch..."
# Push source and build repos.
git push origin gh-pages

echo "Navigating back to the root directory..."
cd ..
