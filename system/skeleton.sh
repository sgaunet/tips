#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

function print_var() {
  echo "${var_value}"
}

function __msg_error() {
    gum log -l error -t DateTime "$1"
}

function __msg_debug() {
    gum log -l debug -t DateTime "$1"
}

function __msg_info() {
    gum log -l info -t DateTime "$1"
}

function handle_exit() {
  # Add cleanup code here
  # for eg. rm -f "/tmp/${lock_file}.lock"
  # exit with an appropriate status code
  __msg_info "Exiting script"
}

trap handle_exit 0 SIGHUP SIGINT SIGQUIT SIGABRT SIGTERM

which gum || {
    __msg_error "Gum is not installed. Please install it to proceed."
    exit 1
}

__msg_error "File could not be found. Cannot proceed"

__msg_debug "Starting script execution with 276MB of available RAM"

__msg_info "Script execution completed successfully"
