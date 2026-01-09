import re
import click
from pathlib import Path

def read_file(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    return text

def add_spaces(text):
    text = re.sub(
    r'\d+\.\d+',
    lambda m: " ".join(m.group(0)),
    text)

    return text

def save_file(text, file_path):
    with open(file_path, "w") as f:
        f.write(text)

@click.command()
@click.option(
    "--analytical_data",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Path to the NMR dataframe",
)


def main(analytical_data: Path):
    file_paths = [f"{analytical_data}/data/src-test.txt", f"{analytical_data}/data/src-train.txt", f"{analytical_data}/data/src-val.txt"]

    for path in file_paths:
        text = read_file(path)

        text = add_spaces(text)

        save_file(text, path)

if __name__ == '__main__':
    main()
