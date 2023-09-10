#!/usr/bin/python3
"""
Fabric script to create and distribute an archive to web servers
"""

import os
from fabric.api import env, run, put, local
from pack_web_static import do_pack
from do_deploy_web_static import do_deploy

# Define the Fabric environment variables
env.hosts = ['34.207.190.83', '52.91.178.39']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def create_new_version():
    """
    Create a new version of the archive locally with my_index.html inside
    """
    # Create a directory for the new version
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Copy 'my_index.html' into the new version directory
    local("cp my_index.html versions/")

    # Create the archive with the new version
    archive_path = do_pack()

    return archive_path

def deploy():
    """
    Create and distribute an archive to web servers
    """
    # Create a new version
    archive_path = create_new_version()
    
    if archive_path is None:
        return False
    
    # Deploy the new version
    deployment_result = do_deploy(archive_path)
    
    if deployment_result:
        return True
    else:
        return False

if __name__ == "__main__":
    deploy()
