#!/bin/bash

# this generates the commands needed to load the datafiles
#  into the divvy_2020 or divvy_2021 tables based upon
#  the year that is in the file name


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

    # the table depends upon the year
    year=1900
    if [[ $1 =~ .*(202[0-9]).* ]]; then
      year=${BASH_REMATCH[1]}
    fi

    if [[ $year -lt 2000 ]]; then
      return
    fi

  table=divvy_$year
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
    for f in Divvy_Trips_2020_Q?.csv; do
      appendTo $f
    done
    for f in 202???-divvy-tripdata.csv; do
      appendTo $f
    done
else
    for f in $*; do
        appendTo $f
    done
fi