#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
import os
from fabric.api import env, run, put

env.hosts = ['34.207.190.83', '100.27.12.119']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]
        remote_tmp_path = "/tmp/{}".format(archive_filename)
        remote_folder = "/data/web_static/releases/{}".format(archive_no_ext)

        put(archive_path, remote_tmp_path)
        run("mkdir -p {}".format(remote_folder))
        run("tar -xzf {} -C {}".format(remote_tmp_path, remote_folder))
        run("rm {}".format(remote_tmp_path))
        run("mv {}/web_static/* {}/".format(remote_folder, remote_folder))
        run("rm -rf {}/web_static".format(remote_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_folder))

        return True
    except Exception as e:
        print("An error occurred: {}".format(str(e)))
        return False
