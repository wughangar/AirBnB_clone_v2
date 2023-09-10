#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""
import os
from fabric.api import run, put, env

env.hosts = ['34.207.190.83', '100.27.12.119']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the web server
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
