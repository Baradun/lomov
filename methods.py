import subprocess
import os as os
import multiprocessing
import json

base_dir = 'main/'

def run(run_file, start, stop, step, method, output_file):
    try:
        result = subprocess.run([
            './' + base_dir + run_file,
            start, stop, step,
            method,
            output_file],
            returncode= 0)
        if result.returncode == 0:
            return 0
        else:
            return RuntimeError
    except subprocess.SubprocessError as e:
        return e

if __name__ == '__main__':








