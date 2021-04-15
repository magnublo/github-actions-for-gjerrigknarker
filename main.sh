#!/bin/bash
(autossh -N -M 0 -o ExitOnForwardFailure=yes -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -R ${lowest_available_port}:127.0.0.1:${PYTHON_PORT} -i /tmp/id_rsa gh_actions_backend@ondehensikter.no) &
$GITHUB_WORKSPACE/webserver.py &
wait -n