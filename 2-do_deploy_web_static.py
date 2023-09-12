#!/usr/bin/python3
"""
Deploy archive!
"""

from fabric.api import put, run, env
import os
import shutil

# Define server IP addresses as a list
server_ips = ['34.207.190.83', '52.91.178.39']

# Set Fabric environment variables
env.user = 'ubuntu'
env.key_filename = '/path/to/your/ssh/key'


# Define local paths and filenames
archive_path = "/AirBnB_clone_v2/test_archive.tgz"
local_html_dir = "/root/web_files"
archive_filename = os.path.basename(archive_path)
archive_no_extension = os.path.splitext(archive_filename)[0]


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


def deploy_locally():
    """Deploy code locally."""
    try:
        # Check if the archive file exists locally
        if not os.path.exists(archive_path):
            print(f"Archive file not found at {archive_path}")
            return False

        # Uncompress the archive locally
        shutil.unpack_archive(archive_path, local_html_dir)

        # Update the symbolic link locally
        local_current_link = os.path.join(local_html_dir, 'current')
        local_new_link = os.path.join(local_html_dir, archive_no_extension)

        if os.path.exists(local_current_link):
            os.unlink(local_current_link)

        os.symlink(local_new_link, local_current_link)

        # Files are now available locally
        print("Local deployment successful!")
        return True
    except Exception as e:
        print("Local deployment failed: {}".format(e))
        return False


if __name__ == '__main__':
    archive_path = input("Enter the path to the archive: ")

    # Deploy remotely
    remote_result = do_deploy(archive_path)

    # Deploy locally
    local_result = deploy_locally()

    if remote_result:
        print("Deployment to remote servers successful")
    else:
        print("Deployment to remote servers failed")

    if local_result:
        print("Local deployment successful")
    else:
        print("Local deployment failed")
