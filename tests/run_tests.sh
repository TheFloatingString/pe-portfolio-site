#!/bin/bash
cd ..
export TESTING=true
python3 -m unittest discover -s tests
echo "Tests Completed"
