#!/usr/bin/env python3
import argparse
import os
import yaml

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--sources',action='store_true')
group.add_argument('--family',action='store_true')
args = parser.parse_args()

with open(os.path.join("sources", "config.yaml")) as config_file:
  config = yaml.load(config_file, Loader=yaml.FullLoader)

if args.family:
	print(config['familyName'])

if args.sources:
	print(" ".join([f"sources/{source}" for source in config['sources']] ))
