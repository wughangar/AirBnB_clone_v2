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
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(archive_name)).failed is True:
        return None
    return archive_name
