import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/peatear-anthony/books_for_study.git'
def deploy():
    site_folder = f'/home/{env.user}/sites/www.staging.petersroom.co/books_for_study/tdd_with_python'
    site_folder_parent = f'/home/{env.user}/sites/www.staging.petersroom.co/books_for_study'
    run(f'mkdir -p {site_folder}')

    with cd(site_folder_parent):
        _get_latest_source()
    with cd(site_folder):
        _update_virtualenv()
        _create_or_udpate_dotenv()
        _udpate_static_files()
        _update_database()


def _get_latest_source():
    cd(f'/home/{env.user}/sites/www.staging.petersroom.co/books_for_study')
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('venv/bin/pip'):
        run(f'python3 -m venv venv')
    run('./venv/bin/pip install -r requirements.txt')


def _create_or_udpate_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = '.join'(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')


def _udpate_static_files():
    run('./venv/bin/python manage.py collectstatic --noinput')


def _update_database():
    run('./venv/bin/python manage.py migrate --noinput')
