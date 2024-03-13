from fabric import task

TEST_CODE_DIR = '~/django-projects/test-osale/foodbank-campaign/src'
PRODUCTION_CODE_DIR = '/www/apache/domains/www.toidupank.ee/django-projects/live-osale/foodbank-campaign/src'

# for FreeBSD compatibility
SHELL = '/bin/sh -c'


@task
def copyproddb(c):
    c.get(f'{PRODUCTION_CODE_DIR}/db.sqlite3')


@task
def deploytest(c):
    c.shell = SHELL
    with c.cd(TEST_CODE_DIR):
        pull_changes(c)
        with c.prefix('. ../venv/bin/activate'):
            update_dependencies(c)
            migrate_database(c)
            update_static_files(c)
            restart_app(c)

def update_dependencies(c):
    c.run('pip install --requirement=requirements.txt --upgrade')

def pull_changes(c):
    c.run('git fetch')
    c.run('git reset --hard origin/master')

def migrate_database(c):
    c.run('python manage.py migrate --noinput')

def update_static_files(c):
    c.run('python manage.py collectstatic --noinput')

def restart_app(c):
    c.run('../scripts/restart-fcgi.sh')
    # for WSGI:
    # c.run('touch toidupank/wsgi.py')
