import subprocess
import sys


def copy_file_to_remote_host(filename, username, remote_host, remote_path):
    cmd = subprocess.Popen(["rsync", "-ave", "{}".format(filename), "{}@{}:{}".format(username, remote_host, remote_path)],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = cmd.stdout.readlines()
    if not result:
        error = cmd.stderr.readlines()
        print >> sys.stderr, "ERROR: %s".format(error)
        return error
    else:
        print(result)
        return result


def execute_over_ssh(command, username, remote_host):
    # assuming keys were exchanged, no password required
    cmd = subprocess.Popen(["ssh", "{}@{}".format(username, remote_host), "{}".format(command)],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = cmd.stdout.readlines()
    if not result:
        error = cmd.stderr.readlines()
        print >> sys.stderr, "ERROR: %s".format(error)
        return error
    else:
        print(result)
        return result
