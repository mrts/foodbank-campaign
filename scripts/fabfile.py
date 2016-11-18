from fabric.api import env, run, cd, prefix

CODE_DIR = '~/django-projects/test-osale/foodbank-campaign/src'

# for FreeBSD compatibility
env.shell = '/bin/sh -c'

def deploy():
    with cd(CODE_DIR):
        pull_changes()
        with prefix('. ../venv/bin/activate'):
            update_dependencies()
            migrate_database()
            update_static_files()
            restart_app()

def update_dependencies():
    run('pip install --requirement=requirements.txt')

def pull_changes():
    run('git fetch')
    run('git reset --hard origin/master')

def migrate_database():
    run('python manage.py migrate')

def update_static_files():
    run('python manage.py collectstatic --noinput')

def restart_app():
    run('../scripts/restart-fcgi.sh')
    # for WSGI:
    # run('touch toidupank/wsgi.py')
