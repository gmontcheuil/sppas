#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    scripts.trsconvert.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    ... a script to export annotations files.

"""
import sys
import os.path
from argparse import ArgumentParser

PROGRAM = os.path.abspath(__file__)
SPPAS = os.path.dirname(os.path.dirname(os.path.dirname(PROGRAM)))
sys.path.append(SPPAS)

from sppas.src.annotationdata.transcription import Transcription
import sppas.src.annotationdata.aio

# ----------------------------------------------------------------------------
# Verify and extract args:
# ----------------------------------------------------------------------------

parser = ArgumentParser(usage="%s -i file -o file [options]" % os.path.basename(PROGRAM),
                        description="... a script to export annotations files.")

parser.add_argument("-i",
                    metavar="file",
                    required=True,
                    help='Input annotated file name')

parser.add_argument("-o",
                    metavar="file",
                    required=True,
                    help='Output annotated file name')

parser.add_argument("-t",
                    metavar="value",
                    required=False,
                    action='append',
                    type=int,
                    help='A tier number (use as many -t options as wanted). '
                         'Positive or negative value: 1=first tier, -1=last tier.')

parser.add_argument("-n",
                    metavar="tiername",
                    required=False,
                    action='append',
                    type=str,
                    help='A tier name (use as many -n options as wanted).')

parser.add_argument("--quiet",
                    action='store_true',
                    help="Disable the verbosity")

if len(sys.argv) <= 1:
    sys.argv.append('-h')

args = parser.parse_args()

# ----------------------------------------------------------------------------
# Read

if args.quiet is False:
    print("Read input file:")
trs_input = sppas.src.annotationdata.aio.read(args.i)
if args.quiet is False:
    print(" [  OK  ]")

# ----------------------------------------------------------------------------
# Select tiers

# Take all tiers or specified tiers
tier_numbers = []
if not args.t and not args.n:
    tier_numbers = range(1, (trs_input.GetSize() + 1))
elif args.t:
    tier_numbers = args.t

# Select tiers to create output
trs_output = Transcription(name=trs_input.GetName())

# Add selected tiers into output
for i in tier_numbers:
    if args.quiet is False:
        print(" -> Tier "+str(i)+":")
    if i > 0:
        idx = i-1
    elif i < 0:
        idx = i
    else:
        idx = trs_input.GetSize()
    if idx < trs_input.GetSize():
        trs_output.Append(trs_input[idx])
        if args.quiet is False:
            print(" [  OK  ]")
    else:
        if not args.quiet:
            print(" [IGNORED] Wrong tier number.")

if args.n:
    for n in args.n:
        t = trs_input.Find(n, case_sensitive=False)
        if t is not None:
            trs_output.Append(t)
        else:
            if not args.quiet:
                print(" [IGNORED] Wrong tier name.")

# Set the other members
trs_output.metadata = trs_input.metadata
# TODO: copy relevant hierarchy links

# ----------------------------------------------------------------------------
# Write

if args.quiet is False:
    print("Write output file:")
sppas.src.annotationdata.aio.write(args.o, trs_output)
if args.quiet is False:
    print(" [  OK  ]")
