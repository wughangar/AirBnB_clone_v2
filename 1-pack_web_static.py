import os
import tarfile
from datetime import datetime
from fabric import task


@task
def do_pack(c):
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

    # Create the .tgz archive with verbose output
    try:
        with c.prefix("cd " + web_static_dir):
            c.local(f"tar -cvzf {os.path.join(versions_dir, archive_name)} .")
        return os.path.abspath(os.path.join(versions_dir, archive_name))
    except Exception as e:
        print(f"Error creating archive: {str(e)}")
        return None
