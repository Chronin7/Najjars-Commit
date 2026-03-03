#!/usr/bin/env python3
"""
Simple converter: load a .glb/.gltf model with Panda3D and write a .bam file.
Usage:
    python convert_glb_to_bam.py input.glb [output.bam]
Or convert all .glb files in a folder:
    python convert_glb_to_bam.py --dir path/to/folder
"""
import sys
import os

from direct.showbase.ShowBase import ShowBase


class Converter(ShowBase):
    def __init__(self):
        # use offscreen to avoid opening a render window
        ShowBase.__init__(self, windowType='offscreen')
        self.disableMouse()

    def convert(self, input_path, output_path):
        print(f"Loading {input_path}...")
        model = self.loader.loadModel(input_path)
        if model is None or model.isEmpty():
            print('Failed to load', input_path)
            return False
        print(f"Writing {output_path}...")
        try:
            model.writeBamFile(output_path)
        except Exception as e:
            print('Failed to write BAM:', e)
            return False
        print('Done')
        return True


def convert_all_in_dir(app, folder):
    converted = []
    for fname in os.listdir(folder):
        lower = fname.lower()
        if not (lower.endswith('.glb') or lower.endswith('.gltf')):
            continue
        inp = os.path.join(folder, fname)
        out = os.path.splitext(inp)[0] + '.bam'
        if os.path.exists(out):
            print('BAM already exists for', inp, '- skipping')
            continue
        ok = app.convert(inp, out)
        if ok:
            converted.append(out)
    return converted


if __name__ == '__main__':
    app = Converter()

    # If no args: convert all .glb/.gltf in CWD
    if len(sys.argv) == 1:
        cwd = os.getcwd()
        print('No args: converting all .glb/.gltf in', cwd)
        converted = convert_all_in_dir(app, cwd)
        print('Converted:', converted)
        sys.exit(0)

    # legacy modes
    if sys.argv[1] == '--dir':
        if len(sys.argv) < 3:
            print('Provide a folder path after --dir')
            sys.exit(1)
        folder = sys.argv[2]
        converted = convert_all_in_dir(app, folder)
        print('Converted:', converted)
        sys.exit(0)

    # single file convert
    inp = sys.argv[1]
    if len(sys.argv) >= 3:
        out = sys.argv[2]
    else:
        out = os.path.splitext(inp)[0] + '.bam'
    ok = app.convert(inp, out)
    sys.exit(0 if ok else 2)
