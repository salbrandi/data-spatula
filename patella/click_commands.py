
''' V Third-Party Packages V '''
import click

''' V Local Packages V '''
import htmlparser


@click.group()
def patella():
    pass

@click.command()
@click.argument('url')
@click.option('--filename', default='dlfile', help='specify the name of the local file that will be downloaded to the current directory')
@click.option('--filetype', default='.csv', help='specify the file type the scraper will look for')
def scrape_url(url, filetype, filename):
    htmlparser.find_download_links(url, filetype, filename)
    click.echo('ERROR: ' + htmlparser.find_download_links(url, filetype, filename))  # Error reporting
    return


@click.command()
@click.argument('newindex')
def change_index(newindex):
    return


@click.command()
@click.argument('column_names')
def change_columns(column_names):
    return


@click.command()
@click.argument('title')
def plot():
    return


@click.command()
@click.argument('url')
@click.argument('fltp')
def testme(url, fltp):
    click.echo(url, fltp)
    return

patella.add_command(scrape_url)
patella.add_command(testme)
