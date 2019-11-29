#!/bin/bash
# Create new repository on github by user and repo.
function github-create() {
    if [[ $# < 1 || ${1} == "-h" || ${1} == "--help" || $# > 2 ]]; then
        echo "Usage: gitclk-create <repository>"
        echo "       gitclk-create <user> <repository>"
        exit 0
    fi

    if [[ $# == 2 ]]; then
        user=${1}
        repository=${2}
    else
        user="lonsty"
        repository=${1}
    fi
    export https_proxy=${https_proxy//https/http}
    curl -u "${user}" https://api.github.com/user/repos -d "{\"name\":\"${repository}\"}"
    export https_proxy=${https_proxy//http/https}
}

github-create "$@"
