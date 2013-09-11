set -e
set -x
if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {database_dump.bz2}"
    exit 2
fi
SQL_ARCHIVE=$1
MYSQL="mysql -uroot -proot"
$MYSQL <<< "drop database djangoplanner; create database djangoplanner"
bzcat $SQL_ARCHIVE | $MYSQL djangoplanner


