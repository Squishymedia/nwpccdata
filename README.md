This contains the Django project for the Northwest Power and Conservation Council
REST data API. See requirements.txt in the NPC folder for Python dependencies.

It is intended to run on a Linux server, and has been deployed to Ubuntu Server
12.04. There's nothing fancy or so custom that it wouldn't work on any Linux server
capable of running Django.

See fabfile.py for deployment tasks and run fab -l in the npc folder to see a list
of available tasks. System prerequisites and dependencies are handled by the Fabric
script command.

Generally, first-time deployment is done like this:

```
fab server_prerequisites
fab web_create_site
fab web_release
```

Subsequent deployments will just use:

```fab web_release```

This hasn't been tested very thoroughly, so it's possible you might have make some
adjustments.

You'll also need to change the user account and server name in fabfile.py, because
it uses mine right now.

Another thing that may come up: some default installations of Nginx don't accept
files more than 1MB. In that case, edit /etc/nginx.conf and set this:

```client_max_body_size 5M;```

- Jason Champion
