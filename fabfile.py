from fabric.api import env, local, run, put, get, cd, sudo
import datetime

env.hosts = ['sitka-stg.sqm.io:22421']
code_dir = '/var/django/'
app_name = 'npc'
db_name = 'db.sqlite3'
init_name = 'npc'

# Deploy the site and database to the server.
def web_release():
    local('tar czf ../django-' + app_name + '.tgz .')
    run('mkdir -p /var/django/npc/')
    put('../django-' + app_name + '.tgz', code_dir + app_name + '/')
    with cd(code_dir + app_name):
        run('tar xzf ./django-' + app_name +'.tgz')
        # Not using south, so this is not necessary
        #run('python manage.py migrate')
        run('rm ./django-' + app_name + '.tgz')
        run('/etc/init.d/django-' + init_name + ' restart')
    local('rm ../django-' + app_name + '.tgz')

# Deploy the web and FastCGI config and restart both the web server and CGI.
# Requires that NGINX be installed on the server.
def web_create_site():
    put('configs/django-npc', '/tmp/django-npc')
    put('configs/fastcgi.conf', '/tmp/fastcgi.conf')
    put('configs/sitka-stg.sqm.io', '/tmp/sitka-stg.sqm.io')
    sudo('mv /tmp/django-npc /etc/init.d/')
    sudo('chmod 755 /etc/init.d/django-npc')
    sudo('mkdir -p /var/django/run/')
    sudo('touch /var/django/run/' + app_name + '.pid')
    sudo('mv /tmp/fastcgi.conf /etc/nginx/')
    sudo('mv /tmp/sitka-stg.sqm.io /etc/nginx/sites-available/')
    sudo('ln -fs /etc/nginx/sites-available/sitka-stg.sqm.io /etc/nginx/sites-enabled/sitka-stg.sqm.io')
    sudo('/etc/init.d/nginx stop')
    sudo('/etc/init.d/django-npc stop')
    # Give the CGI process a chance to stop before starting again.
    run('sleep 4')
    sudo('/etc/init.d/nginx start')
    sudo('/etc/init.d/django-npc start')

# Downloads a copy of the database to the local system
# (sqlite version)
def database_download():
    local('mkdir -p ../bak')
    local('cp ' + db_name + ' ../bak')
    get(code_dir + app_name + '/' + db_name, './' + db_name)

# Takes a bare Linux server and installs prerequisite libraries and software.
def server_prerequisites():
    sudo('sudo apt-get install -y nginx sqlite3 python python-pip postgresql-server-dev-9.1 python-dev')
    put('./requirements.txt', '/tmp/requirements.txt')
    sudo('pip install -r /tmp/requirements.txt')
