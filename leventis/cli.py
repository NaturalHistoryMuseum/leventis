# -*- coding: utf-8 -*-

"""Console script for lev1."""
import sys
import click
import logging
import click_log

from leventis.bhl import BHLCitations


logger = logging.getLogger('leventis')
click_log.basic_config(logger)


@click.group()
def leventis():
    pass


@leventis.command()
@click.option('--binomial', default=None)
def bhl(binomial):
    """
    Download images from BHL
    """
    if binomial:
        click.echo('Downloading {} from BHL'.format(binomial))
    else:
        click.echo('Downloading from BHL')

    logger.setLevel(logging.INFO)

    bhl_citations = BHLCitations()

    images = bhl_citations.get_images()
    print(images)

    # bhl_citations.build_dataframe()

    # bhl_citations.download_images()
    # print(bhl_citations.output_citations_without_urls())


@leventis.command()
@click.option('--binomial', default=None)
def rebuild(binomial):
    """
    OCR an image
    """
    logger.setLevel(logging.INFO)
    bhl_citations = BHLCitations()


if __name__ == "__main__":
    leventis()
