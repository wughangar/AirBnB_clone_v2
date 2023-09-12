#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""

from fabric.api import env, run, put
from os.path import exists
from datetime import datetime

# Define the web server IP addresses
env.hosts = ['34.207.190.83', '52.91.178.39']

def do_pack():
    """
    Create a .tgz archive from the web_static folder.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        run("mkdir -p /data/web_static/releases")

        # Generate the archive name using the current date and time
        now = datetime.now()
        archive_name = "web_static_" + now.strftime('%Y%m%d%H%M%S') + ".tgz"

        # Use the tar command to create the .tgz archive
        run("tar -czvf /data/web_static/releases/{} /data/web_static/current".format(archive_name))

        # Return the archive path if successful
        return "/data/web_static/releases/" + archive_name
    except Exception:
        return None

def do_deploy(archive_path):
    """
    Distribute the archive to web servers and perform deployment.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the web servers
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/
        filename = archive_path.split('/')[-1]
        folder_name = filename.split('.')[0]
        release_path = "/data/web_static/releases/" + folder_name
        run("mkdir -p " + release_path)
        run("tar -xzf /tmp/{} -C {}".format(filename, release_path))

        # Delete the archive from /tmp/
        run("rm /tmp/{}".format(filename))

        # Move to serving directory
        run("mv {}/web_static/* {}/".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))

        # Delete the current symbolic link
        current_link = '/data/web_static/current'
        run("rm -f {}".format(current_link))

        # Create a new symbolic link
        run("ln -s {} {}".format(release_path, current_link))

        return True
    except Exception:
        return False

def deploy():
    """
    Create and distribute an archive to web servers using do_pack and do_deploy.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

