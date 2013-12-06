set -e
set -x
if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {database_dump.bz2i.out}"
    exit 2
fi
SQL_ARCHIVE=$1

./clean-pg.sh
./prepare-pg.sh

bzcat $1|sudo -u postgres psql -d planner -f -
