# -*- coding: utf-8 -*-
import time
import click
import os
import subprocess

DOCKER_MQTT_NAME = 'broker_testing'
DOCKER_DB_NAME = 'database_testing'


def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


setenv('MODE', 'dev')


def up_container(name: str) -> None:
    python_services_cmd = [
        'docker-compose',
        'up',
        '-d',
        name
    ]

    subprocess.call(python_services_cmd)


def down_container(name: str) -> None:
    python_services_cmd = [
        'docker',
        'stop',
        name
    ]

    subprocess.call(python_services_cmd)


@click.group()
def cli():
    pass


@cli.command(help='run tests')
@click.option('--unit', is_flag=True, help='unit tests')
@click.option('--integration', is_flag=True, help='integration tests')
@click.option('--acceptance', is_flag=True, help='acceptance tests')
@click.option('--all', is_flag=True, help='all tetss')
@click.option('--coverage', is_flag=True, help='coverage processing')
@click.option('--browser', is_flag=True, help='open result in browser')
@click.argument('args', nargs=-1)
def test(unit, integration, acceptance, all, coverage, browser, args):
    os.environ['MODE'] = 'test'

    setenv('BROKER_PORT_BINDED', "1886")
    setenv('BROKER_WEBPORT_BINDED', "8887")

    if unit or all:
        os.environ['UNIT_TESTS'] = '1'
    if integration or all:
        os.environ['INTEGRATION_TESTS'] = '1'
        up_container(DOCKER_MQTT_NAME)
        up_container(DOCKER_DB_NAME)
        time.sleep(5)
        from repositories.database.init_db import init_db
        init_db()
    if acceptance or all:
        os.environ['ACCEPTANCE_TESTS'] = '1'

    if coverage:
        python_tests_cmd = [
            'coverage',
            'run',
            '--omit',
            '\'venv/*, test/*\'',
            '-m',
            'unittest',
            'tests/__main__.py',
            # 'tests/unit/domain/test_actuator_observer.py',
            '&&',
            'coverage',
            'html',
            '-d',
            'coverage',
            '&&',
            'coverage',
            'report',
        ]

        if browser:
            python_tests_cmd = python_tests_cmd + [
                '&&',
                'browse',
                'coverage/index.html',
            ]

    else:
        python_tests_cmd = [
            'python',
            '-m',
            'unittest',
            'tests/__main__.py'
        ]

    python_tests_cmd.extend(args)
    subprocess.call(' '.join(python_tests_cmd), shell=True)

    if integration or all:
        down_container(DOCKER_MQTT_NAME)
        down_container(DOCKER_DB_NAME)


if __name__ == '__main__':
    cli()
