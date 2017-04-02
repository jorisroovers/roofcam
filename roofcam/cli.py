import os, fnmatch
from roofcam.classifier import classify_wet_or_dry
from flask import Flask, render_template, send_from_directory
import click

app = Flask(__name__)

# Store the target file in a global file, not ideal but being pragmatic here :)
FILE = None


@click.command()
@click.option('-p', '--port', default=1234, help="Port on which to run web.py [default: 1234]")
@click.option('-h', '--host', default="0.0.0.0", help="Host on which to run web.py [default: 0.0.0.0]")
@click.option('-w', '--web', help="Enable web output", is_flag=True)
@click.option('-f', '--file', help="Classify a single file",
              type=click.Path(exists=True, resolve_path=True, file_okay=True, readable=True))
@click.option('-d', '--dir', help="Classify a directory of files",
              type=click.Path(exists=True, resolve_path=True, file_okay=False, readable=True))
def cli(port, host, web, file, dir):
    #
    if web:
        global FILE
        if file:
            FILE = file
        elif dir:
            files = os.listdir(dir)
            files.sort()
            FILE = os.path.join(dir, files[-1])
        app.run(host=host, port=port)
    else:
        # We're not running a webserver, so just do the classification for the passed file or all files in the
        # passed directory

        if file:
            files = [file]
        else:
            files = fnmatch.filter(os.listdir(dir), "*snapshot*")
            files = [os.path.join(dir, f) for f in files]

        if files:
            for file in files:
                result = classify_wet_or_dry(file)
                print file, "=>", result


@app.route('/snapshot/<snapshot>')
def snapshot(snapshot):
    return send_from_directory(os.path.dirname(FILE), snapshot)


@app.route("/")
def index():
    result = classify_wet_or_dry(FILE)
    return render_template("index.html", snapshot=os.path.basename(FILE), result=result)


if __name__ == "__main__":
    cli()
