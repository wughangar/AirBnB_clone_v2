#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

import os
from fabric.api import env, run
from datetime import datetime
from os.path import exists
from fabric.operations import local, put

env.hosts = ['34.207.190.83', '100.27.12.119']


def do_pack():
    """
    Compresses web_static folder to a .tgz archive
    Returns: Archive path or None on failure
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_" + timestamp + ".tgz"
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_name))
        return archive_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases/ directory
        filename = os.path.basename(archive_path)
        folder_name = '/data/web_static/releases/' + filename.split('.')[0]
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the uploaded archive
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        current_link = '/data/web_static/current'
        run('rm -f {}'.format(current_link))

        # Create a new symbolic link
        run('ln -s {} {}'.format(folder_name, current_link))

        return True
    except Exception:
        return False


def deploy():
    """
    Create and distribute an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
