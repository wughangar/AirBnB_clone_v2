#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers.
"""
from fabric.api import put, run, env
import os

env.hosts = ['34.207.190.83', '52.91.178.39']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    archive_filename = os.path.basename(archive_path)
    archive_no_extension = os.path.splitext(archive_filename)[0]

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}".format
            (archive_no_extension))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_no_extension))
        run("rm /tmp/{}".format(archive_filename))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(archive_no_extension, archive_no_extension))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_no_extension))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_no_extension))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False


if __name__ == '__main__':
    archive_path = input("Enter the path to the archive: ")
    result = do_deploy(archive_path)
    if result:
        print("Deployment successful")
    else:
        print("Deployment failed")
