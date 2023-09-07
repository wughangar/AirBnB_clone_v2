from fabric import task
from datetime import datetime
from fabric.exceptions import CommandFailed


@task
def do_pack(c):
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_" + current_time + ".tgz"
        c.local("mkdir -p versions")
        c.local("tar -czvf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except CommandFailed as e:
        print(f"Failed to create the archive: {e}")
        return None
