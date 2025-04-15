# get options
while test ! -z "$*"
do
  case $1 in
    -rclone_config) rclone_config=$2
      shift;shift;;
    -simulation) simulation="true"
      shift;;
    -src) src=$2
      shift; shift;;
    -dst) dst=$2
      shift; shift;;
    -tmpdir) TMPDIR=$2
      shift; shift;;
    *) echo "ERROR: Bad option $1."
      shift;continue;;
  esac
done

