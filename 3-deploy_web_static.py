#!/usr/bin/python3
"""
Full deployment
"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['34.207.190.83', '52.91.178.39']
env.user = '<ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    fo pack function
    """
    if not os.path.exists("versions"):
        os.makedirs("versions")
    now = datetime.utcnow()
    archive_name = f"versions/web_static_{now.strftime('%Y%m%d%H%M%S')}.tgz"
    result = local(f"tar -cvzf {archive_name} web_static")
    if result.succeeded:
        return archive_name
    else:
        return None

def do_deploy(archive_path):
    """
    do deploy function
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        archive_file = archive_path.split("/")[-1]
        archive_folder = archive_file.split(".")[0]
        run(f"mkdir -p /data/web_static/releases/{archive_folder}/")
        run(f"tar -xzf /tmp/{archive_file} -C /data/web_static/releases/{archive_folder}/")
        run(f"rm /tmp/{archive_file}")
        run(f"mv /data/web_static/releases/{archive_folder}/web_static/* /data/web_static/releases/{archive_folder}/")
        run(f"rm -rf /data/web_static/releases/{archive_folder}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{archive_folder}/ /data/web_static/current")
        return True
    except:
        return False

def deploy():
    """
    do deploy function
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
