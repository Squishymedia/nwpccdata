# Squishy-specific configs

## Missing modules
```sudo pip install djangorestframework
sudo pip install markdown
sudo pip install django-filter
sudo pip install flup
sudo pip install openpyxl```

## modified files
### config/django-npc
Complete rewrite, as the original was Debian/Ubuntu format

### configs/sitka-stg.sqm.io
Fix logging, root paths
```diff
diff --git a/configs/sitka-stg.sqm.io b/configs/sitka-stg.sqm.io
index b05afa4..9936251 100755
--- a/configs/sitka-stg.sqm.io
+++ b/configs/sitka-stg.sqm.io
@@ -1,23 +1,26 @@
 server {
        listen 80;
-       server_name sitka-stg.sqm.io;
+       server_name default;
        rewrite ^/(.*) http://sitka-stg.sqm.io/$1 permanent;
        }

 server {
        listen 80;
        server_name sitka-stg.sqm.io;
-        root /var/django/npc/;
-       access_log off;
-       error_log /var/django/npc.error.log;
+    #    root /var/django/npc/;
+       root /server/www/npcdata/;
+       access_log /var/log/nginx/npc_access.log;
+       error_log /var/log/nginx/npc_error.log;

         location ~ ^/admin/static/ {
-            root /usr/local/lib/python2.7/dist-packages/django/contrib/;
+            #root /usr/local/lib/python2.7/dist-packages/django/contrib/;
+                       root /usr/lib/python2.6/site-packages/django/contrib/;
         }

         location ~* ^.+\.(JPG|JPEG|jpg|jpeg|gif|css|png|js|ico|pdf|zip|exe|wav|gz|bmp|tgz|gz|rar|
-            root /var/django/npc/templates/;
-            access_log off;
+            #root /var/django/npc/templates/;
+                       root /server/www/npcdata/templates/;
+            #access_log off;
             expires 1d;
         }
```

### fabfile.py
Fixed env.hosts to use logged-in user
```diff
diff --git a/fabfile.py b/fabfile.py
index 72db642..f9882aa 100755
--- a/fabfile.py
+++ b/fabfile.py
@@ -1,7 +1,7 @@
 from fabric.api import env, local, run, put, get, cd, sudo
 import datetime

-env.hosts = ['jesse@sitka-stg.sqm.io:22421']
+env.hosts = ['sitka-stg.sqm.io:22421']
 code_dir = '/var/django/'
 app_name = 'npc'
 db_name = 'db.sqlite3'
```
