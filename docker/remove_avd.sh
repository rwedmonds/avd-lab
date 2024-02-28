#!/bin/zsh
#
AVD_IMAGE=$(docker images | grep avd | awk '{print $3}')
docker rmi $AVD_IMAGE

