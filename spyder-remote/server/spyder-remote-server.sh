#!/bin/bash

if [[ $(whoami) != "root" ]]
then
    printf "$0 needs to be executed as root.\\n"
    exit 1
fi

if [[ $CONDA_DEFAULT_ENV != "base" ]]
then
    printf "$0 needs to be executed in the base conda environment. (not $CONDA_DEFAULT_ENV)\\n"
    exit 1
fi


printf "let's install"
