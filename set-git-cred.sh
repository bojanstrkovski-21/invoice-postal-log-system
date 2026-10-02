#!/bin/bash
#
# Sets the Git identity and the origin remote for this repo.
# Based on arch-boki-post-install-dev/set-git-cred.sh.
# Does not change system-wide Git settings and does not use sudo.

project=invoice-postal-log-system

echo "-----------------------------------------------------------------------------"
echo "this is project https://github.com/bojanstrkovski-21/$project"
echo "-----------------------------------------------------------------------------"

git config --global pull.rebase false
git config --global user.name "bojanstrkovski-21"
git config --global user.email "bojanstrkovski.21@gmail.com"
git config --global push.default simple

git remote set-url origin git@github.com:bojanstrkovski-21/$project

echo "Everything set"
echo "Remote is now SSH. Push with ./push.sh"
echo "################################################################"
echo "###################    T H E   E N D      ######################"
echo "################################################################"
