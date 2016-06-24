from fabric.api import run, cd, prefix

CODE_DIR = '/var/www/projects/toidupank/src'


def deploy():
    with cd(CODE_DIR):
        pull_changes()
        with prefix('. ../venv/bin/activate'):
            migrate_database()
            update_static_files()
            restart_app()

def pull_changes():
    run('git pull')

def migrate_database():
    run('python manage.py migrate')

def update_static_files():
    run('python manage.py collectstatic --noinput')

def restart_app():
    run('touch toidupank/wsgi.py')
