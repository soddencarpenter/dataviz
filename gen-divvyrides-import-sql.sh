#!/bin/bash

table=divvy_trips

# OS specific support.  $var _must_ be set to either true or false.
cygwin=false
darwin=false
os400=false
hpux=false
wsl=false
case "`uname`" in
CYGWIN*) cygwin=true;;
Darwin*) darwin=true;;
OS400*) os400=true;;
HP-UX*) hpux=true;;
Linux*)
  redo="`uname -a`"
  case $redo in
    *microsoft*) wsl=true;;
  esac
esac


if $wsl; then
  curdir=$(wslpath -m .)
elif $cygwin; then
  curdir=$(cygpath -f `pwd`)
else
  curdir=`pwd`
fi


function appendTo() {
    local f=$1

cat << EOF
load data infile "${curdir}/$f"
  into table $table
  fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
  ignore 1 rows
  ;

EOF
}


if [[ $# -eq 0 ]]; then
    for f in divvy_trip_history*.csv; do
      appendTo $f
    done
else
    for f in $*; do
        appendTo $f
    done
fi