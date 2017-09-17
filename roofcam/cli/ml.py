import click
from collections import Counter
import json
import os
import sys
from roofcam import classifier

TARGET_STORE_FILE = "target.json"


@click.group()
def cli():
    pass


@cli.command("accuracy")
@click.option('-d', '--dir', required=True, help="Directory containing target.json and images",
              type=click.Path(exists=True, resolve_path=True, file_okay=False, readable=True))
def accuracy(dir):
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
                        # print key, "=>", result, "=?=", val['class']
                else:
                    counters['unknown'] += 1
                    # print key, "=>", result, "=?=", " UNKNOWN"

            except:
                counters['errors'] += 1

    print "\n---------------------------"
    print "SUMMARY"
    print "TOTAL = {0}".format(counters['total'])
    print "CORRECT = {0}".format(counters['correct'])
    print "INCORRECT = {0}".format(counters['total'] - counters['correct'])
    print "ACCURACY = {0}".format(float(counters['correct']) / float(counters['total']))
    print "ERRORS = {0}".format(counters['errors'])
    print "---------------------------"


if __name__ == "__main__":
    cli()
