#!/usr/bin/python3
# fabric script that generates a .gtz archive from the contents

import os
import tarfile
from datetime import datetime
from fabric import task


def do_pack():
    """Generate a .tgz archive from the web_static folder."""

    web_static_dir = '/root/AirBnB_clone/web_static'

    # Ensure the 'versions' directory exists
    versions_dir = os.path.join(web_static_dir, 'versions')
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)

    # Generate a unique archive name based on the current date and time
    now = datetime.utcnow()
    formatted_time = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{formatted_time}.tgz"

    # Create the .tgz archive
    try:
        with tarfile.open(os.path.join(versions_dir,
                                       archive_name), "w:gz") as tar:
            tar.add(web_static_dir, arcname=os.path.basename(web_static_dir))
        return os.path.abspath(os.path.join(versions_dir, archive_name))
    except Exception as e:
        print(f"Error creating archive: {str(e)}")
        return None


if __name__ == "__main__":
    archive_path = do_pack()
    if archive_path:
        print(f"Archive created successfully: {archive_path}")
    else:
        print("Archive creation failed.")
