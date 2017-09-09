import click
import json
import os


@click.group()
def cli():
    pass


@cli.command("compactdb")
@click.option('-d', '--dir', required=True, help="Directory containing target.json and images",
              type=click.Path(exists=True, resolve_path=True, file_okay=False, readable=True))
def compact_db(dir):
    """ Compacts the target.json db file by removing non-existing file entries from it """
    target_file = os.path.join(dir, "target.json")
    if not os.path.exists(target_file):
        click.echo("FATAL: No file '{0}'".format(target_file))
        exit(1)

    print "Compacting db", dir, "..."
    with open(target_file) as json_data:
        db = json.load(json_data)

    for filename in db.keys():
        full_path = os.path.join(dir, filename)
        if not os.path.exists(full_path):
            print "Removing {}".format(filename)
        del db[filename]

    with open(target_file, 'w') as f:
        json.dump(db, f)

    print "DONE"


if __name__ == "__main__":
    cli()
