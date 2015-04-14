# Introduction #

Install nginx
```
apt-get install nginx
/usr/sbin/update-rc.d -f nginx defaults
```

Make a file /etc/nginx/sites-available/planner
```
server {
    listen 80;
    server_name 10.0.20.60;
    access_log /var/log/nginx/planner.access.log;
    error_log /var/log/nginx/planner.error.log;

    location /static/ { # STATIC_URL
        alias /home/planner/venv/gnudok-planner/src/planner/static/;
        expires 30d;
    }

    location /media/ { # MEDIA_URL
        alias /home/planner/venv/gnudok-planner/src/planner/static;
        expires 30d;
    }

    location / {
        include fastcgi_params;
        fastcgi_split_path_info ^()(.*)$;
        fastcgi_pass 127.0.0.1:8080;
    }
}
```
and link to this from /etc/nginx/sites-enabled/planner. Remove the link to default in /etc/nginx/sites-enabled.

Follow HowToBuild to get a working copy in ~planner

Then generate the static files (as planner):
```
$cd ~/venv/gnudok-planner
$bin/django collectstatic
```

Use this startup script:
```
#!/bin/bash
. ~/venv/bin/activate
~/venv/gnudok-planner/bin/django runfcgi host=127.0.0.1 port=8080
```