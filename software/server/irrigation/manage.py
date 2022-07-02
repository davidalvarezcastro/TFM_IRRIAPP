# -*- coding: utf-8 -*-
import click
import os
import subprocess

DOCKER_MQTT_NAME = 'broker_testing'


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
            # 'tests/__main__.py',
            'tests/unit/domain/database/test_dal_area_types.py',
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

    # up_container(DOCKER_MQTT_NAME)
    subprocess.call(' '.join(python_tests_cmd), shell=True)
    # down_container(DOCKER_MQTT_NAME)


if __name__ == '__main__':
    cli()
