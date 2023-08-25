#!/usr/bin/env python3

import os
import sys
import shutil

def decompiler(path, output_dir):
    curdir = os.path.dirname(os.path.realpath(__file__))
    cmd = f"cd {path};java -cp {curdir}/java-decompiler.jar org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -hdc=0 -dgs=1 -rsy=1 -rbr=1 -lit=1 -nls=1 -mpm=60 . ."
    # print(cmd)
    os.system(cmd)

    # Iterate through the decompiled files and move them to the output directory
    for root, _, files in os.walk(path):
        for file in files:
            try:
                if file.endswith(".java"):
                    # Calculate the relative path from the input directory to the current file
                    relative_path = os.path.relpath(os.path.join(root, file), path)
                    # Construct the target path in the output directory
                    target_path = os.path.join(output_dir, relative_path)
                    # Ensure the directory structure exists in the output directory
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    # Move the file to the target path
                    shutil.move(os.path.join(root, file), target_path)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("[Usage:] python3 class2java.py source_directory output_directory")
    else:
        source_directory = sys.argv[1]
        output_directory = sys.argv[2]
        decompiler(source_directory, output_directory)
