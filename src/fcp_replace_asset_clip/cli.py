#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET
from tqdm import tqdm

from . import replace_asset_clips
from fcp_io import fcpxml_io

def main():
    # Define possible arguments
    # fcp-replace-asset-clip --affix='60fps_fixed_' <file_path>
    parser = argparse.ArgumentParser(description="Replaces asset-clip source media without changing the offset, start, and duration of the original asset-clip data.")
    parser.add_argument("fcpxml_filepath", help="Absolute filepath to fcpxml (required)")
    # output
    parser.add_argument("--affix", type=str, default='timescale60_fixed_', help="affix to recognize the replacing media filenames and also used in modifying the output filename")
    # debug
    parser.add_argument("--debug", action='store_true', help="(experimental) display debug messages.")

    args = parser.parse_args()

    xf = fcpxml_io.clean_filepath(args.fcpxml_filepath)
    print(f"fcpxml file: {xf}")

    # <fcpxml>
    tree, root = fcpxml_io.get_fcpxml(xf)
    # '100/6000s'
    fps = fcpxml_io.get_fps(root)
    if args.debug:
        print(f"fps: {fps}")
    """
    The whole point of this tool is that, when not using Apple's expansive default ProRes options, when FCP imports media files into a Library, it seems to internally re-calculates the frame rate using 1000 as the magic number numerator. For example, a 60 fps vfr video is imported as 1000/17 ~ 58.82 fps. Remuxing such 60 fps vfr source media into a constant frame rate (cfr) video of 60 fps is one solution, but it takes up system resources and is potentially not lossless.
    """

    # assets to be replaced in all asset-clips
    target_assets = replace_asset_clips.parse_target(root=root, affix=args.affix, debug=args.debug)

    # replace in all asset-clips
    replace_asset_clips.replace_with_target(root=root, target=target_assets, affix=args.affix, debug=args.debug)

    #blade_silences.collapse_gaps(root=root, fps=fps, debug=args.debug)

    fcpxml_io.save_with_affix(tree=tree, src_filepath=xf, affix=args.affix)

if __name__ == "__main__":
    main()
