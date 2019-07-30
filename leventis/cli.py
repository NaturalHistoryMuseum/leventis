
import click
import logging
import pandas as pd
import mysql.connector as sql
import time
from pathlib import Path
from tqdm import tqdm

from leventis.parse_page import ParsePage

output_path = Path('../output')

logger = logging.getLogger()
logging.basicConfig(filename=output_path / 'trait.log', filemode='w',
                    format='%(levelname)s - %(message)s')


@click.command()
@click.option('--limit', default=None, help='Limit', type=int)
@click.option('--taxon', default=None, help='Filter by taxon')
@click.option('--page', default=None, help='Page ID', type=int)
def main(limit, taxon, page):

    results = {}

    db_connection = sql.connect(database='pup', user='root')

    query = '''
        SELECT bc.page_id, pt.trait_term, pn.pup_name AS taxon
        FROM bhl_citations bc
            INNER JOIN pup_names_sp pn ON pn.pup_name_id = bc.pup_id
            INNER JOIN trait_page tp ON tp.page_id = bc.page_id
            INNER JOIN x_pup_traits pt ON tp.trait_id=pt.trait_id
        WHERE pn.pup_higher_group = 'Dicot' AND bc.item_language = 'English';
    '''

    df = pd.read_sql(query, con=db_connection)

    if taxon:
        df = df[df['taxon'] == taxon]

    df = df.groupby('page_id')['taxon'].agg(set).reset_index()

    if limit:
        df = df[:limit]

    if page:
        df = df[df['page_id'] == page]

    with tqdm(list(df.itertuples(index=False)), leave=True) as bar:
        for page_id, taxa in bar:
            bar.set_description(f"Page {page_id}")

            parsed_page = ParsePage(page_id)

            for taxon in taxa:

                results.setdefault(taxon, {})

                try:
                    results[taxon][page_id] = parsed_page.traits[taxon]
                except KeyError:

                    if taxon not in parsed_page.taxa:
                        logging.warning(
                            f"Taxon {taxon} not found in {page_id}"
                        )
                    else:
                        logging.warning(
                            f"No traits found for {taxon} in {page_id}"
                        )

    results_df = pd.DataFrame(
        zip(results.keys(), results.values()),
        columns=['Taxon', 'Traits']
    )

    results_df.to_csv(output_path / 'traits.csv')

    click.echo(click.style('Trait extraction complete',  fg='green'))

    click.echo(results_df.head(n=20))


if __name__ == '__main__':
    main()
