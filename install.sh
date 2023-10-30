#! /bin/bash

for d in `ls -la | grep ^d | awk '{print $NF}' | egrep -v '^\.'`; do

  python3 $PWD/.src/pybuild/pyall.py $PWD/$d

  case $d in
    *python* ) python3 $PWD/.src/pybuild/pypy.py $PWD/$d ;;
    *java* ) python3 $PWD/.src/pybuild/pyjava.py $PWD/$d ;;
  esac

  ./folder.sh $d

done
