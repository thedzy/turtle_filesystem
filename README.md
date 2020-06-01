# turtle_filesystem.py

![](images/downloads_folder.png =1000x)

Create a visual representation of a folder structure

## What?

Draw the hierarchy of a folder radially.  Customise the visual output and render to screen or file (.ps).

Files are to scale, meaning any file occupying 1% of a ring is the same file same as another occupying 1% of a ring.

```bash
usage: turtle_filesystem.py [-h] [-p PATH_TO_DIR] [-o PATH] [-s SCALE] [-l INTEGER] [-q QUALITY] [-b DECIMAL DECIMAL DECIMAL] [-f DECIMAL DECIMAL DECIMAL]
                            [-x WIDTH] [-y HEIGHT]

Draw filesystem with turtle

optional arguments:
    -h, --help
            show this help message and exit
    -p PATH_TO_DIR, --path PATH_TO_DIR
            Path to visualise
            Default: $HOME/Downloads
    -o PATH, --out-file PATH
            Export to file instead, postscript (.ps)
            Default: None
    -s SCALE, --scale SCALE
            Scale of the visuals
            Default: 10
    -l INTEGER, --line_width INTEGER
            Line width
            Default: 1
    -q QUALITY, --quality QUALITY
            Quality of the curves,
            1 is each line represents 72 degrees
            2 is each line represents 36 degress
            Default: 10
    -b DECIMAL DECIMAL DECIMAL, --colour-back DECIMAL DECIMAL DECIMAL
            3 RGB values of 0.0-1.0
            Note: Does no apply to saved files, change in post
            Default: [1.0, 1.0, 1.0]
    -f DECIMAL DECIMAL DECIMAL, --colour-line DECIMAL DECIMAL DECIMAL
            3 RGB values of 0.0-1.0
            Default: [0.0, 0.0, 0.0]
    -x WIDTH, --width WIDTH
            Width of the window
            Default: 0
    -y HEIGHT, --height HEIGHT
            Height of the window
            Default: 0
```

## Why?
I think the concept is visually neat.

## Improvements?
I don't know if I could have got some more speed improvements, to file is good, but I think the inherently slow nature of turtle drawing to screen is the only slow point.

Colour options.  I have the code for this in another program, just needs to be adapted.

## State?
No known bugs.  Works.

## New
###1.0
Initial commit
