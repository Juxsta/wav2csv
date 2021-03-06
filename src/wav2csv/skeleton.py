"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = wav2csv.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys
import pandas as pd
from scipy.io import wavfile
from pathlib import Path, PosixPath

from wav2csv import __version__

__author__ = "Eric Reyes"
__copyright__ = "Eric Reyes"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from wav2csv.skeleton import fib`,
# when using this Python module as a library.


def fib(samrate,data,input_filename:PosixPath,outputPath):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    # assert n > 0
    # a, b = 1, 1
    # for _i in range(n - 1):
    #     a, b = b, a + b
    # return a
    def output_filename (suffix): 
        output = outputPath if outputPath else input_filename.parent
        return str(output / (input_filename.name[:-4]+suffix))
    wavData = pd.DataFrame(data)
    _logger.info("Converting wav data")
    _logger.debug(wavData)

    if len(wavData.columns) == 2:
        print('Stereo .wav file\n')
        wavData.columns = ['R', 'L']
        stereo_R = pd.DataFrame(wavData['R'])
        stereo_L = pd.DataFrame(wavData['L'])
        _logger.info('Saving...\n')
        stereo_R.to_csv(output_filename("_Output_stereo_R.csv") , mode='w')
        stereo_L.to_csv(output_filename("_Output_stereo_L.csv" ), mode='w')
        # wavData.to_csv("Output_stereo_RL.csv", mode='w')
        _logger.debug('Save is done ' + output_filename("_Output_stereo_R.csv") 
                            + output_filename("_Output_stereo_L.csv" ))

    elif len(wavData.columns) == 1:
        _logger.info('Mono .wav file\n')
        wavData.columns = ['M']

        wavData.to_csv(output_filename("_Output_mono.csv"), mode='w')

        _logger.info('Save is done ' + output_filename('_Output_mono.csv'))

    else:
        _logger.info('Multi channel .wav file\n')
        _logger.info('number of channel : ' + len(wavData.columns) + '\n')
        wavData.to_csv(output_filename("Output_multi_channel.csv"), mode='w')

        _logger.info('Save is done ' + output_filename('Output_multi_channel.csv'))

    return 

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Convert wav file to csv")
    parser.add_argument(
        "--version",
        action="version",
        version="DevDockers {ver}".format(ver=__version__),
    )
    parser.add_argument(dest="wavFile", help="n-th Fibonacci number", type=lambda p: Path(p).absolute(), metavar="wavfile.wav")
    parser.add_argument("-o", "--output", dest="outputPath", help="Output Path Folder", type=lambda p: Path(p).absolute(), metavar="~/wav_csvs")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """



    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug(args)
    wavdata = wavfile.read(args.wavFile)
    _logger.info("Wav File Imported properly")

    fib(*wavdata,args.wavFile,args.outputPath)
    # print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))
    _logger.info("Script Complete")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m wav2csv.skeleton 42
    #
    run()
