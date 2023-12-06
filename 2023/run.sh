day=$1
part=$2
[ -z "$part" ] && {
  >&2 echo 'usage: ./run.sh dayXX partY'
  exit 1
}

idris2 $day/$part.idr -p contrib -x main < $day/file.txt
