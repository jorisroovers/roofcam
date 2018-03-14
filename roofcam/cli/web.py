import os
import fnmatch
import json
import traceback
from roofcam import classifier
from flask import Flask, render_template, send_from_directory, request, jsonify
import click

from collections import OrderedDict

TARGET_STORE_FILE = "target.json"

web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../web")
template_dir = os.path.join(web_dir, "templates")
static_dir = os.path.join(web_dir, "static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@click.command()
@click.option('-p', '--port', default=1234, help="Port on which to run web.py [default: 1234]")
@click.option('-h', '--host', default="0.0.0.0", help="Host on which to run web.py [default: 0.0.0.0]")
@click.option('--debug', help="Enable debug mode", is_flag=True)
@click.option('-d', '--dir', help="Directory of images to serve", required=True,
              type=click.Path(exists=True, resolve_path=True, file_okay=True, readable=True))
def cli(port, host, debug, dir):
    app.config['PATH'] = dir
    app.config['TARGET_CLASS_STORE'] = os.path.join(dir, TARGET_STORE_FILE)
    app.run(host=host, port=port, debug=debug)


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
        prediction = classifier.classify_wet_or_dry(
            os.path.join(app.config['PATH'], snapshot))
    except Exception as e:
        prediction = "ERROR ({0})".format(str(e))
        traceback.print_exc()  # let's print traceback for debugging

    if target is None:
        target = get_target(snapshot)
    return {'snapshot': snapshot, 'prediction': prediction, 'target': target}


def available_snapshot_dates():
    snapshot_grouping = OrderedDict()
    for image in image_list():
        date = image.replace("snapshot-", "").split("_")[0]
        date_snapshot_list = snapshot_grouping.get(date, [])
        date_snapshot_list.append(image)
        snapshot_grouping[date] = date_snapshot_list

    return snapshot_grouping


@app.route('/snapshot/<snapshot>')
def snapshot(snapshot):
    dirname = app.config['PATH']
    if not os.path.isdir(app.config['PATH']):
        dirname = os.path.dirname(app.config['PATH'])

    if snapshot.lower() == "latest":
        snapshot = image_list()[-1]

    return send_from_directory(dirname, snapshot)


@app.route('/snapshotdata/<snapshot>')
def snapshotdata(snapshot):
    if snapshot.lower() == "latest":
        snapshot = image_list()[-1]
    return jsonify(snapshot_data(snapshot))


@app.route('/prev/<snapshot>')
def prev_snapshot(snapshot):
    files = image_list()
    prev_index = max(files.index(snapshot) - 1, 0)
    file = files[prev_index]
    return jsonify(snapshot_data(file))


@app.route('/next/<snapshot>')
def next_snapshot(snapshot):
    files = image_list()
    next_index = min(files.index(snapshot) + 1, max(len(files) - 1, 0))
    file = files[next_index]
    return jsonify(snapshot_data(file))


@app.route('/classify/<snapshot>', methods=['POST'])
def classify(snapshot):
    data = {}
    if os.path.exists(app.config['TARGET_CLASS_STORE']):
        with open(app.config['TARGET_CLASS_STORE']) as data_file:
            data = json.load(data_file)

    data[snapshot] = {'class': request.form['class']}

    with open(app.config['TARGET_CLASS_STORE'], 'w') as outfile:
        json.dump(data, outfile, indent=4)

    return jsonify(snapshot_data(snapshot, target=request.form['class']))


@app.route("/")
def index():
    prediction = snapshot_data(image_list()[-1])
    return render_template("index.html", available_snapshot_dates=available_snapshot_dates(), **prediction)


if __name__ == "__main__":
    cli()
