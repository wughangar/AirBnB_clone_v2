#!/usr/bin/python3
"""
Deploy archive!
"""

from fabric.api import put, run, env
import os

# Define server IP addresses as a list
server_ips = ['34.207.190.83', '52.91.178.39']

# Set Fabric environment variables
env.user = 'ubuntu'
env.key_filename = '/path/to/your/ssh/key'


def do_deploy(archive_path):
    """Distribute an archive to web servers."""

    # Check if the archive file exists
    if not os.path.exists(archive_path):
        print(f"Archive file not found at {archive_path}")
        return False

    # Set the hosts dynamically based on server_ips
    env.hosts = server_ips

    archive_filename = os.path.basename(archive_path)
    archive_no_extension = os.path.splitext(archive_filename)[0]

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the specified folder
        run("mkdir -p /data/web_static/releases/{}"
            .format(archive_no_extension))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(archive_filename, archive_no_extension))

        # Clean up and create symbolic links
        run("rm /tmp/{}"
            .format(archive_filename))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}"
            .format(archive_no_extension, archive_no_extension))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_no_extension))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current"
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
