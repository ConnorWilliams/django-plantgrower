# Plant Grower
Django project and django-plantgrower app

## Uses
- Django
- Django Channels for websockets
- Django REST framework for API
- Python Celery for periodic tasks and task queue
- Redis for Channels and Celery backend

## Deployment
### Nginx proxy configuration
In `/etc/nginx/sites-available/plantgrower`:

```
# Websockets: For NGINX to send the Upgrade request from the client to the backend server,
# the Upgrade and Connection headers must be set explicitly.

http {
  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }

  server {
    listen 80;

    location / {
      proxy_pass http://0.0.0.0:8001;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
    }
  }
}
```

Then run `ln -s /etc/nginx/sites-available/plantgrower /etc/nginx/sites-enabled/` to enable the site.

### Systemd service config for running circus on boot
In `/lib/systemd/system/circus.service`:
```
[Unit]
Description=Circus process manager
After=syslog.target network.target nss-lookup.target

[Service]
Type=simple
ExecReload=/usr/bin/circusctl reload
ExecStart=/usr/local/bin/circusd /home/pi/plant_grower/plantgrower.ini
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Then run `systemctl enable circus`, possibly with `sudo`.


### Logrotate configuration
In `/etc/logrotate.d/plantgrower`:

```
/var/log/plantgrower/*.log {
    su pi pi
    daily
    missingok
    rotate 14
    compress
    notifempty
    create 0644 pi pi
}
```

## TODO
- [ ] [Django secure production deployment checklist](https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/)
- [ ] Finish unit tests
