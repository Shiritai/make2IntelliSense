# this script runs command and safe into files
import os

def cmd_stream(cmd: str) -> list[str]:
    """ Stream command output line by line """
    stream = os.popen(cmd)
    stm = stream.read()
    return stm.split('\n')

def open_or_stream(file_path: str, cmd: str) -> list[str]:
    """
    Open a file to stream strings.
    If file does not exist, then run cmd to get streaming string
    """
    ret: list[str]
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            ret = f.readlines()
    else:
        ret = cmd_stream(cmd)
    return ret