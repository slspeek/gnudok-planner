# Build instructions on Debian Wheezy #
Install mercurial version control system, create user planner and grant planner unlimited sudo rights
```
#apt-get install mercurial git
#adduser planner
#su - planner
```

Clone the source
```
hg clone https://code.google.com/p/gnudok-planner/
```

Navigate in the source folder
```
cd gnudok-planner
sh install-tool-chain.sh
sh install-pg-tool-chain.sh
cd ..
virtualenv --no-site-packages venv
mv gnudok-planner venv
source venv/bin/activate
cd venv/gnudok-planner
pip install --upgrade setuptools
python bootstrap.py
bin/buildout
```

## Prepare mysql ##
```
cat db_init.sql |mysql -u root -p
```
## Prepare postgres ##
```
sh prepare-pg.sh
```
Give two times 'planner'
## Run the tests ##
```
bin/django test -v 3
```

## Install postalcode database ##
```
wget http://6pp.kvdb.net/exports/mysql_sql.txt.gz
zcat mysql_sql.txt.gz |mysql -uroot -p nlpostcode
```

## How to run a test server ##

### Preparation ###
```
bin/django collectstatic
bin/django syncdb
bin/django migrate
```

### Run it ###
```
bin/django runserver 
```