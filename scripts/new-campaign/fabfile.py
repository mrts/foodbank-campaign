import datetime

from fabric import task

PRODUCTION_CODE_DIR = '/www/apache/domains/www.toidupank.ee/django-projects/live-osale/foodbank-campaign/src'

# for FreeBSD compatibility
SHELL = '/bin/sh -c'


@task
def newcampaign(c, old_start_date, new_start_date):
    # verify that arguments are valid dates
    datetime.date.fromisoformat(old_start_date)
    datetime.date.fromisoformat(new_start_date)
    c.shell = SHELL
    with c.cd(PRODUCTION_CODE_DIR):
        print('>>> Backing up database')
        backup_database(c)
        with c.prefix('. ../venv/bin/activate'):
            print('>>> Printing and removing shift leaders (see shift-leaders.txt)')
            print_and_remove_shift_leaders(c)
            print('>>> Changing shift dates')
            change_shift_dates(c, old_start_date, new_start_date)
            print('>>> Removing volunteers')
            remove_volunteers(c)
            print('>>> Updating and activating campaign')
            update_and_activate_campaign(c, new_start_date)


def backup_database(c):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
    c.run(f'cp db.sqlite3 ../../backups/{timestamp}-db.sqlite3')


def print_and_remove_shift_leaders(c):
    c.run('python utils/new-campaign-print-and-remove-shift-leaders.py')
    c.get(f'{PRODUCTION_CODE_DIR}/shift-leaders.txt')
    c.run('rm -f shift-leaders.txt')


def change_shift_dates(c, old_start_date, new_start_date):
    c.run(f'python utils/new-campaign-change-shift-dates.py {old_start_date} {new_start_date}')


def remove_volunteers(c):
    c.run(f'python utils/new-campaign-remove-volunteers.py')


def update_and_activate_campaign(c, new_start_date):
    c.run(f'python utils/new-campaign-update-and-activate-campaign.py {new_start_date}')
