#!/usr/bin/python3
# bash script

from fabric.api import local
import os.path
from datetime import datetime

def do_pack():
    """
    function to generate .tgx from webstatic content directory
    """
    now = datetime.utcnow()
    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                                 now.month,
                                                                 now.day,
                                                                 now.hour,
                                                                 now.minute,
                                                                 now.second)
    if not os.path.exists("versions"):
        local("mkdir -p versions")

    result = local("LC_ALL=C tar -cvJf {} web_static".format(archive_name))
    if result.failed:
        return None
    return archive_name
