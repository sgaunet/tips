#!/usr/bin/env bash


images=(
    "teleport-9.3.26"
    "teleport-10.3.16"
    "teleport-11.3.22"
)

for image in ${images[@]}; do
    component="${image%-*}"
    version="${image#*-}"
    echo "component: $component"
    echo "version: $version"
done
