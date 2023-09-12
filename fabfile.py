from fabric import task, Connection
import os

# Set the server IP addresses as a list
server_ips = ['34.207.190.83', '52.91.178.39']

@task
def do_deploy(c, archive_path):
    """Distribute an archive to web servers."""
    
    # Check if the archive file exists
    if not os.path.exists(archive_path):
        print(f"Archive file not found at {archive_path}")
        return False
    
    try:
        # Upload the archive to the /tmp/ directory of each web server
        for server_ip in server_ips:
            with Connection(host=server_ip, user='ubuntu') as conn:
                # Upload the archive to the /tmp/ directory of the web server
                conn.put(archive_path, "/tmp/")
    
                # Extract archive to /data/web_static/releases/
                filename = os.path.basename(archive_path)
                folder_name = filename.split('.')[0]
                release_path = f'/data/web_static/releases/{folder_name}/'
                conn.run(f'mkdir -p {release_path}')
                conn.run(f'tar -xzf /tmp/{filename} -C {release_path}')
    
                # Delete the archive from /tmp/
                conn.run(f'rm /tmp/{filename}')
    
                # Move to serving directory
                conn.run(f"mv /data/web_static/releases/{folder_name}/web_static/* /data/web_static/releases/{folder_name}/")
                conn.run(f"rm -rf /data/web_static/releases/{folder_name}/web_static")
    
                # Delete the current symbolic link
                current_link = '/data/web_static/current'
                conn.run(f'rm -f {current_link}')
    
                # Create a new symbolic link
                conn.run(f'ln -s {release_path} {current_link}')
    
                print(f"New version deployed to {server_ip}!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
