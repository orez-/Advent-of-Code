day=$1
part=$2
filename="${3:-file.txt}"
[ -z "$part" ] && {
  >&2 echo 'usage: ./run.sh dayXX partY [testfile.txt]'
  exit 1
}

idris2 $day/$part.idr -p contrib -x main < $day/$filename
