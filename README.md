# Phantom3 .srt Customizer
This scipt helps to customize the .srt file of a DJI Phantom 3.

## Works with
* DJI Phantom 3 Professional
* Please test this script with other models and send a report to continue this list.

## Requrirements
* Python: https://www.python.org/
* pysrt: https://pypi.python.org/pypi/pysrt

## Installation
Just download the file phantom3-srt-customizer.py and use it.

## Run
Run from command line:

    python3 phantom3-srt-customizer.py -h                       (git)-[master]
    usage: phantom3-srt-customizer.py [-h] -i INPUT -o OUTPUT [-hb] [-hu] [-da]
                                      [-ti] [-du] [-sp] [-l]

    This scipt helps to customize the .srt file of a DJI Phantom 3.

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            input .srt file
      -o OUTPUT, --output OUTPUT
                            output .srt file
      -hb, --barometer      add barometer height
      -hu, --ultrasonic     add ultrasonic height
      -da, --date           add date of flight
      -ti, --time           add time of flight
      -du, --duration       add duration of flight
      -sp, --speed          add speed
      -l, --label           add text label to each piece of data

## Example
Command:

    python3 phantom3-srt-customizer.py -i DJI_0001.SRT -o DJI_0001.c.SRT -hb -hu -da -ti -du -sp -l

DJI_0001.SRT:

    ...
    66
    00:01:06,000 --> 00:01:07,000
    HOME(X) 2015.10.18 12:23:23
    GPS(X) BAROMETER:45.9 ULTRASONIC:10.2
    ISO:100 Shutter:800 EV:+1/3 Fnum:F2.8
    ...

DJI_0001.c.SRT:

    ...
    66
    00:01:06,000 --> 00:01:07,000
    Date: 2015.10.18; Time: 12:23:23; Duration: 01:05; Speed: 11.12m/s; Height (b): 45.9m; Height (u): 10.2m;
    ...
