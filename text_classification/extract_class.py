# Script for extracting all strings from a Parquet file belonging to a class.
#
# Author: Saul Johnson <saul.johnson@nhlstenden.com>
# Usage: python extract_class.py --file=<path> --target-class=<class> [--label-column, --target-column]

import click

import pandas as pd


@click.command()
@click.option('--file', type=click.STRING, help='The file to extract from.')
@click.option('--label-column', type=click.STRING, default='label', help='The name of the column containing class labels.')
@click.option('--target-column', type=click.STRING, default='text', help='The name of the column containing values to extract.')
@click.option('--target-class', type=click.STRING, help='The target class to extract.')
def main(file: str, label_column: str, target_column: str, target_class: str):
    """ The main function/entrypoint for the script.
    """
    dataset = pd.read_parquet(file)
    extracted = [row for _, row in dataset.iterrows() if str(row[label_column]) == target_class]
    for row in extracted:
        print(row[target_column])


if __name__ == '__main__':
    main()
