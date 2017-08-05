import os, fnmatch, json, traceback
from roofcam import classifier
from flask import Flask, render_template, send_from_directory, request, jsonify
import click

app = Flask(__name__)


# Store the target PATH in a global var, not ideal but being pragmatic here :)

@click.command()
@click.option('-p', '--port', default=1234, help="Port on which to run web.py [default: 1234]")
@click.option('-h', '--host', default="0.0.0.0", help="Host on which to run web.py [default: 0.0.0.0]")
@click.option('-w', '--web', help="Enable web output", is_flag=True)
@click.option('--debug', help="Enable debug mode", is_flag=True)
@click.option('-f', '--file', help="Classify a single file",
              type=click.Path(exists=True, resolve_path=True, file_okay=True, readable=True))
@click.option('-d', '--dir', help="Classify a directory of files",
              type=click.Path(exists=True, resolve_path=True, file_okay=False, readable=True))
def cli(port, host, web, debug, file, dir):
    #
    if web:
        if file:
            app.config['PATH'] = file
        elif dir:
            app.config['PATH'] = dir
            app.config['TARGET_CLASS_STORE'] = os.path.join(dir, "target.json")
        app.run(host=host, port=port, debug=debug)
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
                try:
                    result = classifier.classify_wet_or_dry(file)
                    print file, "=>", result
                except Exception as e:
                    print file, "=> ERROR", e.message


def image_list():
    return sorted([f for f in os.listdir(app.config['PATH']) if f.endswith(".jpg")])


def get_target(snapshot):
    data = {}
    if os.path.exists(app.config['TARGET_CLASS_STORE']):
        with open(app.config['TARGET_CLASS_STORE']) as data_file:
            data = json.load(data_file)
    return data.get(snapshot, {}).get('class', "UNKNOWN")


def snapshot_data(snapshot, target=None):
    try:
        prediction = classifier.classify_wet_or_dry(os.path.join(app.config['PATH'], snapshot))
    except Exception as e:
        prediction = "ERROR ({0})".format(str(e))
        traceback.print_exc()  # let's print traceback for debugging

    if target is None:
        target = get_target(snapshot)
    return jsonify({'snapshot': snapshot, 'prediction': prediction, 'target': target})


@app.route('/snapshot/<snapshot>')
def snapshot(snapshot):
    dirname = app.config['PATH']
    if not os.path.isdir(app.config['PATH']):
        dirname = os.path.dirname(app.config['PATH'])
    return send_from_directory(dirname, snapshot)


@app.route('/prev/<snapshot>')
def prev_snapshot(snapshot):
    files = image_list()
    prev_index = max(files.index(snapshot) - 1, 0)
    file = files[prev_index]
    return snapshot_data(file)


@app.route('/next/<snapshot>')
def next_snapshot(snapshot):
    files = image_list()
    next_index = min(files.index(snapshot) + 1, max(len(files) - 1, 0))
    file = files[next_index]
    return snapshot_data(file)


@app.route('/classify/<snapshot>', methods=['POST'])
def classify(snapshot):
    data = {}
    if os.path.exists(app.config['TARGET_CLASS_STORE']):
        with open(app.config['TARGET_CLASS_STORE']) as data_file:
            data = json.load(data_file)

    data[snapshot] = {'class': request.form['class']}

    with open(app.config['TARGET_CLASS_STORE'], 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return snapshot_data(snapshot, target=request.form['class'])


@app.route("/")
def index():
    path = app.config.get('PATH')
    file = path
    target = "UNKNOWN"
    if os.path.isdir(path):
        snapshot = image_list()[-1]
        file = os.path.join(path, snapshot)
        target = get_target(snapshot)

    prediction = classifier.classify_wet_or_dry(file)
    return render_template("index.html", snapshot=os.path.basename(file), prediction=prediction, target=target)


if __name__ == "__main__":
    cli()
