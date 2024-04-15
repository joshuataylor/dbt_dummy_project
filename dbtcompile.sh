#!/bin/bash
# this is a stupid/hacky/temporary way to get mise to get the current env.
cd $1
eval "$(mise hook-env)"
python dbtcompile.py -s $2