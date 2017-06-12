import click
import htmlparser

@click.group()
def patella():
    pass

@click.command()
@click.argument('url')
@click.argument('filetype')
@click.option('--filename', default='dataf.tsv', help='specify the name of the local file that will be downloaded to the current directory')
@click.option('--filetype', default='.tsv', help='specify the file type the scraper will look for')
def scrape_url(url, filetype):
    echo('Dataframe loaded to webservice')
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
def graph():
    return


@click.command()
@click.argument('url')
@click.argument('fltp')
def testme(url, fltp):
    htmlparser.find_download_links(url, fltp, 'testfile')
    click.echo('ERROR: ' + htmlparser.find_download_links(url, fltp, 'testfile'))  #Error reporting
    return


if __name__ == '__main__':
    testme()
