#!/usr/bin/env python3
"""
Script:	turtle_filesystem.py
Date:	2020-06-01	

Platform: macOS/Windows/Linux

Description:

"""
__author__ = 'thedzy'
__copyright__ = 'Copyright 2020, thedzy'
__license__ = 'GPL'
__version__ = '1.0'
__maintainer__ = 'thedzy'
__email__ = 'thedzy@hotmail.com'
__status__ = 'Development'

import argparse
import colorsys
import turtle
from pathlib import Path, PurePath


def main():
    if options.path:
        base = options.path
    else:
        base = Path('~/Downloads/').expanduser()
    print('Starting at: ', base)

    # Convert file structure to dictionary
    dir_dict = get_dir_as_dict(base)

    # Use 1000 if your computer uses base10 for size calculations
    print('Directory size: {:0.3f} {}'.format(dir_dict['total_size'] / 1024 / 1024, 'MB'))

    draw(base, dir_dict)


def draw(base, filesystem=None):
    """
    Draw the visualisation
    :param base: (string) Path to start the visualisation
    :param filesystem: (dict) Filesystem
    :return: (void)
    """
    def dict_depth(d):
        if isinstance(d, dict):
            return 1 + (max(map(dict_depth, d.values())) if d else 0)
        return 0

    depth = dict_depth(filesystem)

    # Set the window screen and bounds
    width, height = options.width, options.height
    if width == 0:
        width = (depth + 1) * options.scale * 4
        width = 120 if width < 120 else width
    if height == 0:
        height = width
    turtle.getscreen().setup(width, height)

    # Setup canvas and pen
    turtle.title(base)
    turtle.width(options.line_width / 100)
    turtle.pencolor(*options.colour_line)
    turtle.bgcolor(*options.colour_back)

    # Setup drawing
    turtle.up()
    if options.file:
        turtle.tracer(10000)
    else:
        turtle.tracer(500)
    turtle.hideturtle()

    def draw_segment(size, start, percent, level, colour=None):
        """
        Draw a segment based on position and size
        :param size: (float) Arc value of the size of the segment
        :param start: (float) 0-1 for the starting position of the segment
        :param percent: (float) 0-1 for the size of the segment
        :param level: (int) The segments ring position
        :param colour: (float, float, float) HSV value of the segment
        :return: (void)
        """
        if not colour:
            # Hue is set by mid point in segment, saturation and value by depth
            colour = colorsys.hsv_to_rgb((start + (percent/2)) * 2, 1 - (level / depth / 8), 1 - (level / depth))
        turtle.fillcolor(colour)

        # Reset
        turtle.home()
        turtle.left(360 * start)
        turtle.forward(size * level)
        turtle.left(90)

        # Start draw
        turtle.down()
        turtle.begin_fill()

        # Create shape
        turtle.circle(size * level, 360 * percent, int(percent * options.quality * 5) + 1)
        turtle.right(90)
        turtle.forward(size)
        turtle.right(90)
        turtle.circle((-size * level) - size, 360 * percent, int(percent * options.quality * 5) + 1)
        turtle.right(90)
        turtle.forward(size)

        # End draw
        turtle.end_fill()
        turtle.up()

    def get_segment(sub_dict, level=1, previous_size=1, start=0):
        """
        Get the segment sizes and position and call them to be drawn
        :param sub_dict: (dict) Filesystem
        :param level: (int) Ring level (0 being centre)
        :param previous_size: (float) Size from the previous parent
        :param start: (float) Starting position of the segment
        :return:
        """
        if isinstance(sub_dict, dict):
            start_pos = start
            for sub_key in sub_dict:
                if sub_key is 'total_size':
                    continue

                try:
                    size_self = sub_dict[sub_key]['total_size']
                except (KeyError, TypeError):
                    size_self = sub_dict[sub_key]

                scaled_size = size_self / sub_dict['total_size'] * previous_size
                draw_segment(options.scale * 2, start_pos, scaled_size, level)
                get_segment(sub_dict[sub_key], level + 1, size_self / sub_dict['total_size'] * previous_size, start_pos)
                start_pos += scaled_size

    # Recurse directory tree dictionary
    get_segment(filesystem)

    # Write to file or display
    if options.file:
        turtle.getscreen().getcanvas().postscript(file=options.file.name)
    else:
        turtle.mainloop()

    print('Drawing complete')


def get_dir_as_dict(base):
    """
    Convert a folder structure to a dictionary with calculated size values
    :param base: (string) Path of folder
    :return: (dict)
    """
    # Initialise
    dir_dict = {}

    # Traverse to build out the structure
    directories = list(Path(base).rglob('**'))
    for directory in directories:
        relative_path = Path(directory).relative_to(Path(base))
        sub_dict = dir_dict
        for item in PurePath(relative_path).parts:
            if item not in sub_dict:
                sub_dict[item] = {}
            sub_dict = sub_dict[item]

    # Reverse traverse to fill in the sizes
    for directory in reversed(directories):
        relative_path = Path(directory).relative_to(Path(base))
        sub_dict = dir_dict
        for item in PurePath(relative_path).parts:
            sub_dict = sub_dict[item]

        # Get the sum of all the files
        sum_of_files = 0
        for child in Path(directory).iterdir():
            child_path = Path(directory, child)
            if child_path.is_file():
                size = child_path.stat().st_size
                sub_dict[child.name] = size
                sum_of_files += size

        # Get the sum of all the child directories, using values from the child dicts
        sum_of_dirs = 0
        for key in sub_dict:
            if isinstance(sub_dict[key], dict):
                sum_of_dirs += sub_dict[key]['total_size']

        # Append the sum of the files and directory
        sub_dict['total_size'] = sum_of_files + sum_of_dirs

    return dir_dict


if __name__ == '__main__':
    def parser_formatter(format_class, **kwargs):
        """
        Use a raw parser to use line breaks, etc
        :param format_class: (class) formatting class
        :param kwargs: (dict) kwargs for class
        :return: (class) formatting class
        """
        try:
            return lambda prog: format_class(prog, **kwargs)
        except TypeError:
            return format_class

    def parser_directory(path):
        """
        Handle directory path
        :param path: (string) Path
        :return: Path, exception
        """
        if Path(path).is_dir():
            return path
        else:
            raise argparse.ArgumentTypeError(path)

    parser = argparse.ArgumentParser(description='Draw filesystem with turtle',
                                     formatter_class=parser_formatter(argparse.RawTextHelpFormatter,
                                                                      indent_increment=4, max_help_position=12,
                                                                      width=160))

    # Path
    parser.add_argument('-p', '--path', type=parser_directory,
                        action='store', dest='path',
                        metavar='PATH_TO_DIR',
                        help='Path to visualise\n'
                             'Default: $HOME/Downloads')

    # File
    parser.add_argument('-o', '--out-file', type=argparse.FileType('w'),
                        action='store', dest='file', default=None,
                        metavar='PATH',
                        help='Export to file instead, postscript (.ps)\n'
                             'Default: %(default)s')

    # Visualisation size (drawn/saved)
    parser.add_argument('-s', '--scale', type=int,
                        action='store', dest='scale', default=10,
                        metavar='SCALE',
                        help='Scale of the visuals\n'
                             'Default: %(default)s')
    parser.add_argument('-l', '--line_width', type=int,
                        action='store', dest='line_width', default=1,
                        metavar='INTEGER',
                        help='Line width\n'
                             'Default: %(default)s')
    parser.add_argument('-q', '--quality', type=int,
                        action='store', dest='quality', default=10,
                        metavar='QUALITY',
                        help='Quality of the curves,\n'
                             '1 is each line represents 72 degrees\n'
                             '2 is each line represents 36 degrees\n'
                             'Default: %(default)s')
    parser.add_argument('-b', '--colour-back', type=float,
                        action='store', dest='colour_back', default=[1.0, 1.0, 1.0], nargs=3,
                        metavar='DECIMAL',
                        help='3 RGB values of 0.0-1.0\n'
                             'Note: Does no apply to saved files, change in post\n'
                             'Default: %(default)s')
    parser.add_argument('-f', '--colour-line', type=float,
                        action='store', dest='colour_line', default=[0.0, 0.0, 0.0], nargs=3,
                        metavar='DECIMAL',
                        help='3 RGB values of 0.0-1.0\n'
                             'Default: %(default)s')

    # Window size
    parser.add_argument('-x', '--width', type=int,
                        action='store', dest='width', default=0,
                        metavar='WIDTH',
                        help='Width of the window\n'
                             'Default: %(default)s')
    parser.add_argument('-y', '--height', type=int,
                        action='store', dest='height', default=0,
                        metavar='HEIGHT',
                        help='Height of the window\n'
                             'Default: %(default)s')

    options = parser.parse_args()

    main()

