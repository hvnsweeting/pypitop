#!/usr/bin/env python
# coding: utf-8

'''
Simple script for getting top N most downloaded packages from Pypi
'''

import argparse
import itertools
import xmlrpclib

MAIN_AUDIENCES = [
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
]


class PypiTop(object):
    def __init__(self, no_of_pkgs=20):
        self.client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
        self.toppkgs = self.client.top_packages(no_of_pkgs)
        self.auds_pkgs = self._get_audiences_pkg_map(self.toppkgs)

    def _get_audiences_pkg_map(self, toppkgs):
        audiences_pkgs = {c: set() for c in MAIN_AUDIENCES}
        for pkg, _ in toppkgs:
            version = self.client.package_releases(pkg)[0]
            data = self.client.release_data(pkg, version)
            audiences = [c for c in data['classifiers']
                         if 'Intended Audience' in c]

            for c, pkgs in audiences_pkgs.iteritems():
                if c in audiences:
                    pkgs.add(pkg)

        return audiences_pkgs

    def display_by_audience(self, audience=None):
        print '*' * 30
        if audience is None:
            print 'All packages'
        else:
            print ('Audience: {0}'.format(audience).replace(
                   'Intended Audience ::', ''))

        for pkg, download in self.toppkgs:
            if audience is None or pkg in self.auds_pkgs[audience]:
                print '{0}: {1} downloads'.format(pkg, download)

    def display_all(self):
        for aud in itertools.chain([None], MAIN_AUDIENCES):
            self.display_by_audience(aud)


if __name__ == "__main__":
    argp = argparse.ArgumentParser()
    argp.add_argument('N', type=int, nargs='?', default=20,
                      help='Number of packages')
    args = argp.parse_args()

    pypitop = PypiTop(args.N)
    pypitop.display_all()
