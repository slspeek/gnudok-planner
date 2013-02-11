create database djangoplanner;
create database nlpostcode;
grant all on djangoplanner.* to djangoplanner@'localhost' identified by 'djangoplanner';
grant all on test_djangoplanner.* to djangoplanner@'localhost' identified by 'djangoplanner';
grant all on nlpostcode.* to nlpostcode@'localhost' identified by 'nlpostcode';
grant all on test_nlpostcode.* to nlpostcode@'localhost' identified by 'nlpostcode';
flush privileges;
