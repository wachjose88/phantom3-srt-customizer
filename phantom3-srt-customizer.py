#!/ usr/bin/env python
# -*- coding : utf -8 -*-

# Phantom3 .srt Customizer
#
# Copyright 2015 Josef Wachtler
#
# phantom3-srt-customizer.py

"""
This scipt helps to customize the .srt file of a DJI Phantom 3.
"""

import pysrt
import argparse
import sys
import datetime
import re
from math import radians, cos, sin, asin, sqrt


EARTH_RADIUS = 6371

LABELS = {
          'height_barometer': 'Height (b):',
          'height_ultrasonic': 'Height (u):',
          'date': 'Date:',
          'time': 'Time:',
          'duration': 'Duration:',
          'speed': 'Speed:',
}


def format_output(label, use_label, text):
    """
    Returns formated text.

    Keyword  arguments:
        label -- label key
        use_label -- true if label should be added
        text -- text to format
    """
    t = str(text) + '; '
    if use_label:
        t = LABELS[label] + ' ' + t
    return t


def haversine(src_lon, src_lat, dst_lon, dst_lat):
    """
    Calculate the great circle distance between two gps coordinates
    using the haversine formula.

    Keyword  arguments:
        src_lon -- source longitude in degrees
        src_lat -- source latitude in degrees
        dst_lon -- destination longitude in degrees
        dst_lat -- destination latitude in degrees
    """
    dst_lon, dst_lat, src_lon, src_lat = map(radians,
                                             [dst_lon, dst_lat,
                                              src_lon, src_lat])
    distance_lon = dst_lon - src_lon
    distance_lat = dst_lat - src_lat
    ha = sin(distance_lat/2)**2 + (cos(src_lat) * cos(dst_lat) *
                                   sin(distance_lon/2)**2)
    return (2 * asin(sqrt(ha))) * EARTH_RADIUS


def filter_height(token, ultrasonic, use_label):
    """
    Returns the height.

    Keyword  arguments:
        token -- token to parse
        ultrasonic -- use ultrasonic instead of barometer
        use_label -- true if label should be added
    """
    search = 'BAROMETER'
    label = 'height_barometer'
    if ultrasonic:
        search = 'ULTRASONIC'
        label = 'height_ultrasonic'
    if token.startswith(search):
        h = token.split(':')
        return format_output(label, use_label, h[1] + 'm')
    else:
        return ''


def filter_date(token, use_label):
    """
    Returns the date.

    Keyword  arguments:
        token -- token to parse
        use_label -- true if label should be added
    """
    try:
        d = datetime.datetime.strptime(token, '%Y.%m.%d')
        return format_output('date', use_label, d.strftime('%Y.%m.%d'))
    except ValueError:
        return ''


def filter_time(token, use_label):
    """
    Returns the time.

    Keyword  arguments:
        token -- token to parse
        use_label -- true if label should be added
    """
    try:
        d = datetime.datetime.strptime(token, '%H:%M:%S')
        return format_output('time', use_label, d.strftime('%H:%M:%S'))
    except ValueError:
        return ''


def filter_gps(token):
    """
    Returns the gps as (lon,lat)

    Keyword  arguments:
        token -- token to parse
    """
    if token.startswith('GPS'):
        h = re.split('\(|,|\)', token)
        return (float(h[1]), float(h[2]))
    else:
        return None


def compute_speed(token, use_label):
    """
    Returns the speed.

    Keyword  arguments:
        token -- token to parse
        use_label -- true if label should be added
    """
    try:
        lon, lat = filter_gps(token=token)
        if compute_speed.last_lon is None:
            compute_speed.last_lon = lon
        if compute_speed.last_lat is None:
            compute_speed.last_lat = lat
        distance = haversine(compute_speed.last_lon, compute_speed.last_lat,
                             lon, lat) * 1000
        compute_speed.last_lon = lon
        compute_speed.last_lat = lat
        return format_output('speed', use_label,
                             '%sm/s' % round(distance, 2))
    except:
        return ''
compute_speed.last_lon = None
compute_speed.last_lat = None


def compute_duration(token, use_label):
    """
    Returns the duration.

    Keyword  arguments:
        token -- token to parse
        use_label -- true if label should be added
    """
    try:
        d = datetime.datetime.strptime(token, '%H:%M:%S')
        if compute_duration.first is None:
            compute_duration.first = d
        t = d - compute_duration.first
        minutes, seconds = divmod(int(t.total_seconds()), 60)
        return format_output('duration', use_label,
                             '%02d:%02d' % (minutes, seconds))
    except ValueError:
        return ''
compute_duration.first = None


def main():
    """
    This is the main method. It inits and executes the argparser.
    Loops over all subs
    """
    parser = argparse.ArgumentParser(
        description='This scipt helps to customize '
        'the .srt file of a DJI Phantom 3.')
    parser.add_argument('-i', '--input',
                        help='input .srt file', required=True)
    parser.add_argument('-o', '--output',
                        help='output .srt file', required=True)
    parser.add_argument('-hb', '--barometer', action='store_true',
                        help='add barometer height')
    parser.add_argument('-hu', '--ultrasonic', action='store_true',
                        help='add ultrasonic height')
    parser.add_argument('-da', '--date', action='store_true',
                        help='add date of flight')
    parser.add_argument('-ti', '--time', action='store_true',
                        help='add time of flight')
    parser.add_argument('-du', '--duration', action='store_true',
                        help='add duration of flight')
    parser.add_argument('-sp', '--speed', action='store_true',
                        help='add speed')
    parser.add_argument('-l', '--label', action='store_true',
                        help='add text label to each piece of data')
    args = parser.parse_args()

    if not (args.barometer or args.ultrasonic or args.date or args.time or
            args.duration or args.speed):
        print('Please specify some data to add!\n')
        parser.print_help()
        return -1

    subs = pysrt.open(args.input)

    for s in subs:
        t = ''
        for token in re.split(' |\n', s.text):
            if args.barometer or args.ultrasonic:
                t += filter_height(token=token, ultrasonic=args.ultrasonic,
                                   use_label=args.label)
            if args.date:
                t += filter_date(token=token, use_label=args.label)
            if args.time:
                t += filter_time(token=token, use_label=args.label)
            if args.duration:
                t += compute_duration(token=token, use_label=args.label)
            if args.speed:
                t += compute_speed(token=token, use_label=args.label)

        s.text = t

    subs.save(args.output, encoding='utf-8')
    return 0


if __name__ == "__main__":
    sys.exit(main())

