#!/bin/bash

#python setup.py build

if [ -f Build/exe.win-amd64-2.7/RabbitHole.log ]; then
    rm Build/exe.win-amd64-2.7/RabbitHole.log
fi

python setup.py bdist_msi