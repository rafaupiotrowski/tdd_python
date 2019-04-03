from fabric import task, Connection
from patchwork.files  import append, exists
#from fabric import env, local, run
import random

REPO_URL = 'https://github.com/rafaupiotrowski/tdd_python.git'

@task
def deploy(c):
	c = Connection(
		host='rafalpiotrowski.com.pl', #"18.194.207.228",
		user = 'ubuntu',
		connect_kwargs={
			"key_filename": "/Users/wioletanytko/documents/workspace/awskey.pem",
		},
	)
	site_folder = '/home/%s/sites/%s' % ('rafal', 'rafalpiotrowski.com.pl')
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(c,site_folder)
	_get_latest_source(c,source_folder)
	_update_settings(c,source_folder) #, env.host)
	_update_virtualenv(c,source_folder)
	_update_static_files(c,source_folder)
	_update_database(c,source_folder)

def _create_directory_structure_if_necessary (c,site_folder):
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
		c.run('mkdir -p %s/%s' % (site_folder, subfolder))
        
def _get_latest_source(c,source_folder):
	if exists(c,source_folder + '/.git'):
		c.run('cd %s && git fetch' % (source_folder,))
	else:
		c.run('git clone %s %s' % (REPO_URL, source_folder))
	current_commit = c.local('git log -n 1 --format=%H')
	c.run('cd %s && git reset --hard ' % (source_folder))

def _update_settings (c,source_folder): #, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	c.run("sed -i 's/{stary}/{nowy}/' {nazwa_pliku}".format(stary ="DEBUG = True", nowy="DEBUG = False", nazwa_pliku=settings_path))
	c.run('sed -i "s/{stary}/{nowy}/" {nazwa_pliku}'.format(
	stary ="ALLOWED_HOSTS = \[]",
	nowy ="ALLOWED_HOSTS = [{allowed_hosts}]".format(allowed_hosts ="'rafalpiotrowski.com.pl', 'localhost'"),
	nazwa_pliku=settings_path))
	secret_key_file = source_folder + '/superlists/secret_key.py'
	if not exists(c,secret_key_file):
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(c,secret_key_file, 'SECRET_KEY = "{insert_key}"'.format(insert_key = key))
	append(c,settings_path, '\nfrom .secret_key import SECRET_KEY')
	print('zakonczono update_settings')

def _update_virtualenv(c,source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(c,virtualenv_folder + '/bin/pip'):
		c.run('virtualenv --python=python3 %s' % (virtualenv_folder,))
	c.run ('%s/bin/pip install -r %s/requirements.txt' % (
		virtualenv_folder, source_folder
	))  
	print('zakonczono update_virtualenv')
    
def _update_static_files(c,source_folder):
	c.run('cd {input_source_folder} && ../virtualenv/bin/python3 manage.py collectstatic --noinput'.format(input_source_folder =source_folder,
	))
	print('zakonczono update_static_file')

def _update_database(c,source_folder):
	c.run('cd {input_source_folder} && ../virtualenv/bin/python3 manage.py migrate --noinput'.format(
		input_source_folder=source_folder,
	))
	print('zakonczono update_database')
