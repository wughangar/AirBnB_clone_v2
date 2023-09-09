#!/usr/bin/python3
import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Get the current timestamp for the archive name
    now = datetime.utcnow()

    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                                 now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second)
    
    # Create the "versions" directory if it doesn't exist
    if not os.path.exists("versions"):
        local("mkdir -p versions")

    # Create the .tgz archive
    result = local("tar -cvzf {} web_static".format(archive_name))

    if result.failed:
        return None

    return archive_name
