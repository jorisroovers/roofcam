import click
import fnmatch
from collections import Counter
import json
import os
import sys
from roofcam import classifier

TARGET_STORE_FILE = "target.json"


@click.group()
def cli():
    pass


@cli.command("classify")
@click.option('-D', '--debug', help="Enable debug mode", is_flag=True)
@click.option('-p', '--path', help="Classify a file or directory",
              type=click.Path(exists=True, resolve_path=True, file_okay=True, readable=True))
def classify(debug, path):

    classifier.set_debug(debug)

    if os.path.isfile(path):
        files = [path]
    else:
        files = fnmatch.filter(os.listdir(path), "*snapshot*")
        files = [os.path.join(path, f) for f in files]

    results = []
    for file in files:
        try:
            result = classifier.classify_wet_or_dry(file)
            if debug:
                print file, "=>", result
            results.append({file: {"class": result}})
        except Exception as e:
            if debug:
                print file, "=>", result
            results.append({file: {"class": "ERROR (%s)".format(e.message)}})

    print json.dumps(results)


@cli.command("accuracy")
@click.option('-D', '--debug', help="Enable debug mode", is_flag=True)
@click.option('-d', '--dir', required=True, help="Directory containing target.json and images",
              type=click.Path(exists=True, resolve_path=True, file_okay=False, readable=True))
def accuracy(debug, dir):
    sys.stdout.write("Determining accuracy")
    target = os.path.join(dir, TARGET_STORE_FILE)
    counters = Counter()
    with open(target) as data_file:
        data = json.load(data_file)
        for key, val in data.iteritems():
            sys.stdout.write(".")
            sys.stdout.flush()
            counters['total'] += 1
            try:
                result = classifier.classify_wet_or_dry(os.path.join(dir, key))
                if 'class' in val:
                    if result == val['class']:
                        counters['correct'] += 1
                    else:
                        counters['incorrect'] += 1
                        if debug:
                            print key, "=>", result, "=?=", val['class']
                else:
                    counters['unknown'] += 1
                    if debug:
                        print key, "=>", result, "=?=", " UNKNOWN"

            except KeyboardInterrupt:
                print "Keyboard interrupt. Exiting"
                break
            except:
                counters['errors'] += 1

    print "\n---------------------------"
    print "SUMMARY"
    print "TOTAL = {0}".format(counters['total'])
    print "CORRECT = {0}".format(counters['correct'])
    print "INCORRECT = {0}".format(counters['total'] - counters['correct'])
    print "UNKNOWN = {0}".format(counters['unknown'])
    print "ACCURACY = {0}".format(float(counters['correct']) / float(counters['total']))
    print "ERRORS = {0}".format(counters['errors'])
    print "---------------------------"


if __name__ == "__main__":
    cli()
