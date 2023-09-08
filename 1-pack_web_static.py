#!/usr/bin/python3
# Fabric scripts that generates a.tgz arcgive from web_stactic contents


from fabric import task
from datetime import datetime
import os

WEB_STATIC_PATH = '~/AirBnB_clone/web_static'


@task
def do_pack(c):
    """
    compressing contents fo webstatic
    """
    # creating versions directory if it doesnt exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    archive_name = f"web_static_{timestamp}.tgz"

    # create the archive file
    result = c.local(f"tar - czvf versions/{archive_name}
                     - C {WEB_STATIC_PATH} .")

    if result.failed:
        return None
    else:
        return f"versions/{archive_name}"


if __name__ == "__main__":
    result = do_pack()
    if result:
        print(f"New version packed: {result}")
    else:
        print("Packaging failed.")
