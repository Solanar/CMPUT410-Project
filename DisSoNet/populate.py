#!/usr/bin/env python

#import just python things


def populate():
    #testing data
    pass


if __name__ == '__main__':
    print("Starting DisSoNet database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DisSoNet.settings')
    #import DisSoNet things
    populate()
