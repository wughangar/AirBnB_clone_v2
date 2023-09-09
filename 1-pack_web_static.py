#!/usr/bin/python3
import os
<<<<<<< HEAD
from fabric.api import local
=======
from fabric.api import local, lcd
>>>>>>> 1278033a17c5d989620d58668c921a25aadb0f8f
from datetime import datetime

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
<<<<<<< HEAD
    # Create the 'versions' directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")
=======
    # Get the absolute path to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the absolute path to the 'versions' directory
    versions_dir = os.path.join(script_dir, 'versions')

    # Get the absolute path to the 'web_static' directory
    web_static_dir = os.path.join(script_dir, 'web_static')
>>>>>>> 1278033a17c5d989620d58668c921a25aadb0f8f

    # Get the current timestamp for the archive name
    now = datetime.utcnow()
    archive_name = f"versions/web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"

    # Use the tar command to create the .tgz archive
    result = local(f"tar -cvzf {archive_name} web_static")

<<<<<<< HEAD
    # Check if the tar command was successful
    if result.succeeded:
        return archive_name
    else:
        return None
=======
    archive_name = "{}/web_static_{}{}{}{}{}{}.tgz".format(versions_dir,
                                                           now.year,
                                                           now.month,
                                                           now.day,
                                                           now.hour,
                                                           now.minute,
                                                           now.second)
    
    # Create the "versions" directory if it doesn't exist
    if not os.path.exists(versions_dir):
        local("mkdir -p {}".format(versions_dir))

    # Change to the "web_static" directory and create the .tgz archive
    with lcd(web_static_dir):
        result = local("tar -cvzf {} .".format(archive_name))

    if result.failed:
        return None

    return archive_name
>>>>>>> 1278033a17c5d989620d58668c921a25aadb0f8f
