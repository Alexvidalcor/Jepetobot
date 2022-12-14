#!/bin/bash

if [ $( docker ps -a | grep appcontainer | wc -l ) -gt 0 ]; then
    echo "appcontainer exists"
    docker stop appcontainer_cont
    docker rm appcontainer_cont
else
        echo "testContainer does not exist"
fi
