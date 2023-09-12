i#!/usr/bin/python3
""" Deploy existing web_static_20230911113338.tgz to servers """

from fabric.api import env, put, sudo, run
from os.path import exists

env.hosts = ['34.207.190.83', '52.91.178.39', '127.0.0.1']

def do_deploy(archive_path):
    """
    Distribute the existing archive to web servers and perform deployment.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the existing archive to /tmp/ on the web servers
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
        sudo(f"mv {release_path}web_static/* {release_path}")
        sudo(f"rm -rf {release_path}web_static")
        
        # Delete the current symbolic link
        current_link = '/data/web_static/current'
        sudo(f'rm -f {current_link}')
        
        # Create a new symbolic link
        sudo(f'ln -s {release_path} {current_link}')

        return True
    except Exception as e:
        print(e)
        return False
