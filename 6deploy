#!/usr/bin/python3
""" 2-do_deploy_web_static """

from fabric.api import env, put, sudo, local
from os.path import exists
from datetime import datetime
env.hosts = ['34.207.190.83', '52.91.178.39', '127.0.0.1']


def do_pack():
    """
    Create a .tgz archive from the web_static folder.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive name using the current date and time
        now = datetime.now()
        archive_name = f"web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"

        # Use the tar command to create the .tgz archive
        local(f"tar -czvf versions/{archive_name} web_static")

        # Return the archive path if successful
        return f"versions/{archive_name}"
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
        release_path = f'/data/web_static/releases/{folder_name}/'
        sudo(f'mkdir -p {release_path}')
        sudo(f'tar -xzf /tmp/{filename} -C {release_path}')

        # Delete the archive from /tmp/
        sudo(f'rm /tmp/{filename}')
        # Move to serving directory
        sudo(f"mv /data/web_static/releases/{folder_name}/web_static/* /data\
/web_static/releases/{folder_name}/")
        sudo(f"rm -rf /data/web_static/releases/{folder_name}/web_static")
        # Delete the current symbolic link
        current_link = '/data/web_static/current'
        sudo(f'rm -f {current_link}')

        # Create a new symbolic link
        sudo(f'ln -s {release_path} {current_link}')

        return True
    except Exception:
        return False
