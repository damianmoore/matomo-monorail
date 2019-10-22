# Matomo Monorail

This is a Django app to try and make [Matomo Analytics](https://matomo.org/) more accurate. Some users will have JavaScript or trackers disabled so they don't show up in Matomo. However, we can collect a coarser level of data when we serve dynamic pages.


## How it works

This project's middleware collects requests in a similar way to standard webserver logs. The tricky part is that we only want to import these logs into Matomo when there are no requests logged by the tracking JavaScript. We achieve this by proxying the Matomo JS client requests via a Django view too. A background job then analyses the logs, only making API calls to Matomo itself if there was no proxied traffic for the request.


## Usage

You will need Motomo installed. For development purposes you can use the included Docker Compose file. You will still need to do some setup and get the generated API auth token.

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
