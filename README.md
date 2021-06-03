# Matomo Monorail

This is a Django app to try and make [Matomo Analytics](https://matomo.org/) more accurate. Some users will have JavaScript or trackers disabled so they don't show up in Matomo. However, we can collect a coarser level of data when we serve dynamic pages.


## How it works

This project's middleware collects requests in a similar way to standard webserver logs. The tricky part is that we only want to import these logs into Matomo when there are no requests logged by the tracking JavaScript. We achieve this by proxying the Matomo JS client requests via a Django view too. A background job then analyses the logs, only making API calls to Matomo itself if there was no proxied traffic for the request.


## Usage

You will need Motomo installed. For development purposes you can use the included Docker Compose file. You will still need to do some setup and get the generated API auth token (Administration > API).

    docker-compose up

There some dependencies (namely, `requests`). You can get a virtual environment quickly setup using `pipenv`.

    pipenv install
    pipenv shell

Using the example project, you can see it work. You will want edit the settings in `example_project/example/settings.py` to configure it to your Matomo installation. A page that includes the Matomo tracking code is at [http://localhost:8000/](http://localhost:8000/) and one that doesn't (which should still send to Matomo) is at [http://localhost:8000/no-js-tracking/](http://localhost:8000/no-js-tracking/).

    cd example_project
    python manage.py migrate
    python manage.py runserver

To do the analysis of logged requests and send the ones that were "server only" to Matomo's API, you need to run this Django management command.

    python manage.py upload_requests -d

In production you should use a reverse proxy to handle your static content so these requests do not get logged.


## Settings

These need to be in your Django `settings.py` file set to the values relating to your real Matomo instance:

    MATOMO_BASE_URL = 'http://localhost:8001/'
    MATOMO_SITE_ID = 1
    MATOMO_TOKEN_AUTH = 'a35b4469f1c38d222822a32a413b1991'

You need to add `matomo_monorail` to `INSTALLED_APPS`:

    INSTALLED_APPS = [
        ...
        'matomo_monorail',
    ]

You need to add the `matomo_monorail.middleware.RequestLoggingMiddleware` middleware to log incoming requests:

    MIDDLEWARE = [
        ...
        'matomo_monorail.middleware.RequestLoggingMiddleware',
    ]


## Other configuration

As this works as a proxy through to your real Matomo instance, you have to hook these URLs up to views in your `urls.py`. Make sure to update your Matomo JS tracking code to route traffic through the same server.

    from matomo_monorail.views import proxy_js, proxy_php

    urlpatterns = [
        path('matomo.js', proxy_js),
        path('matomo.php', proxy_php),
        ...
    ]


## Building

Bump up the version number in `setup.py` then build the Python source package:

    python setup.py sdist

Tag and push Git commit as version:

    git commit -m ...
    git tag vX.X.X
    git push origin --tags


## Troubleshooting

### Correct IP address of user

You need to make sure the IP address of the user is being passed through any proxies you may have in front of your Django server. If this is not passed through, you will get a server-logged address of something like `127.0.0.1` that doesn't match any client-logged addresses and a duplicate visit will be sent to Matomo's API. The code extracting the IP address checks if `request.META.get('HTTP_X_FORWARDED_FOR')` exists.

Example minimal Nginx configuration to pass forwarded IP address to Django:

```
location / {
    proxy_pass        http://localhost:8000;
    proxy_set_header  X-Forwarded-For $proxy_add_x_forwarded_for;
}
```

### Correct HTTP scheme (HTTPS) of user

Another possible way you might get duplicates showing up in Matomo is if the users access your site via `https://` but the connection from your reverse proxy to Django is plain `http://`. Aparently the inverse can happen as well if the connection from your reverse proxy to Django is secure. To solve this there are two things you need to do: 1) add a header in your proxy to pass the scheme to Django, 2) Tell Django which header and it's value determine `request.is_secure()` to equal `True`.

Example minimal Nginx configuration to pass forwarded scheme to  Django:

```
location / {
    proxy_pass        http://localhost:8000;
    proxy_set_header  X-Forwarded-Proto $scheme;
}
```

Example Django setting:

``` python
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Multiple proxies stripping headers

It's possible your setup has ore than one layer of proxying before you hit Django. This is especially try If you are living in a containerised world. Where you have to use header settings above to pass client IP and scheme, make sure this is done ONLY at the outermost layer (which the client will hit). Otherwise you are likely to overwrite the headers you already set and will end up with just an internal IP address and `HTTP` rather than `HTTPS` scheme.
