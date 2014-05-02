server {
	listen 80;
	server_name www.squishy.sitkatech.com;
	rewrite ^/(.*) http://squishy.sitkatech.com/$1 permanent;
	}

server {
	listen 80;
	server_name squishy.sitkatech.com;
        root /var/django/npc/;
	access_log off;
	error_log /var/django/npc.error.log;

        location ~ ^/admin/static/ {
            root /usr/local/lib/python2.7/dist-packages/django/contrib/;
        }

        location ~* ^.+\.(JPG|JPEG|jpg|jpeg|gif|css|png|js|ico|pdf|zip|exe|wav|gz|bmp|tgz|gz|rar|txt|tar|rtf)$ {
            root /var/django/npc/templates/;
            access_log off;
            expires 1d;
        }

        location / {
                client_body_timeout 600;
                send_timeout 600;
                fastcgi_read_timeout 600;
                fastcgi_pass 127.0.0.1:9000;
                fastcgi_param PATH_INFO $fastcgi_script_name;
                include /etc/nginx/fastcgi.conf;
                fastcgi_param QUERY_STRING $query_string;
                fastcgi_param REQUEST_METHOD $request_method;
                fastcgi_param CONTENT_TYPE $content_type;
                fastcgi_param CONTENT_LENGTH $content_length;
                fastcgi_pass_header Authorization;
                fastcgi_intercept_errors off;
        }

}
