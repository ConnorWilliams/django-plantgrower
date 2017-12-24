# Plant Grower
Django project intended for django-plantgrower app

## Uses
- Django
- Channels for websockets
- Beatserver for running a periodic job which sends info over WS to front end
- JS for wesockets on front end
- django-bootstrap3 CSS
- django-dashing for nice dashboard

## Intended application
django-plantgrower cutom plant grower app

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

### Circus config for supervising Daphne and workers


## Channels Info
When you want to enable channels in production, you need to do three things:

1. Set up a channel backend (Redis). See CHANNEL_LAYERS in settings.py. This is what asgi_redis is for.
2. Run worker servers - the work of running consumers is decoupled from the work of talking to HTTP. Workers don’t open any ports, all they do is talk to the channel backend (Redis). Use [Circus](http://circus.readthedocs.io/en/latest/usecases/) to keep them up and running. One per core is usually good. For deploying new code you can just restart the worker servers with sigterm which will cleanly exit and unhandled requests will be sent to new workers.
3. Run interface servers (Daphne) - They do the work of taking incoming requests and loading them into the channels system.

## TODO
- [ ] [Logging](https://docs.djangoproject.com/en/2.0/topics/logging/)
- [ ] [Circus](http://circus.readthedocs.io/en/latest/usecases/) for process monitoring on workers and interface server
- [ ] [Django secure production deployment checklist](https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/)
- [ ] Finish unit tests
