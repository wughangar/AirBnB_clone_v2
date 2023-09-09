#!/usr/bin/python3
import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the 'versions' directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Get the current timestamp for the archive name
    now = datetime.utcnow()
    archive_name = f"versions/web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"

    # Use the tar command to create the .tgz archive
    result = local(f"tar -cvzf {archive_name} web_static")

    # Check if the tar command was successful
    if result.succeeded:
        return archive_name
    else:
        return None
