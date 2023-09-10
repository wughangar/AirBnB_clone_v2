#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

import os
from fabric.api import env, run
from os.path import exists
from fabric.operations import local, put
from pack_web_static import do_pack
from do_deploy_web_static import do_deploy

env.hosts = ['34.207.190.83', '100.27.12.119']

def deploy():
    """
    Create and distribute an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
