#!/usr/bin/python3
"""
Deploy archive!
"""

from fabric.api import put, run, env
import os

# Set the server IP addresses as a list
server_ips = ['34.207.190.83', '52.91.178.39']

# Set Fabric environment variables
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distribute an archive to web servers."""

    # Check if the archive file exists
    if not os.path.exists(archive_path):
        print(f"Archive file not found at {archive_path}")
        return False

    # Set the hosts dynamically based on server_ips
    env.hosts = server_ips

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Extract archive to /data/web_static/releases/
        filename = os.path.basename(archive_path)
        folder_name = filename.split('.')[0]
        release_path = f'/data/web_static/releases/{folder_name}/'
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')

        # Delete the archive from /tmp/
        run(f'rm /tmp/{filename}')

        # Move to serving directory
        run(f"mv /data/web_static/releases/{folder_name}/web_static/* /data/web_static/releases/{folder_name}/")
        run(f"rm -rf /data/web_static/releases/{folder_name}/web_static")

        # Delete the current symbolic link
        current_link = '/data/web_static/current'
        run(f'rm -f {current_link}')

        # Create a new symbolic link
        run(f'ln -s {release_path} {current_link}')

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False


if __name__ == '__main__':
    archive_path = input("Enter the path to the archive: ")

    # Deploy remotely
    remote_result = do_deploy(archive_path)

    if remote_result:
        print("Deployment to remote servers successful")
    else:
        print("Deployment to remote servers failed")
