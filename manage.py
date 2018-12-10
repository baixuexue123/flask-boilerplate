import click

from app import create_app

app = create_app()


@click.group()
def cli():
    pass


@click.command()
@click.option('--host', default='0.0.0.0', type=str)
@click.option('--port', default=8888, type=int)
def runserver(host, port):
    click.echo('runserver...')
    app.run(host='0.0.0.0', port=8888, debug=True, threaded=True)


cli.add_command(runserver)


if __name__ == '__main__':
    cli()
