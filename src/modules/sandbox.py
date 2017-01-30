import docker, os
from requests.exceptions import ReadTimeout

class Sandbox(object):
    def __init__(self, src_file_path, ip_file_path):
        self.client = docker.APIClient(base_url='unix://var/run/docker.sock')
        self.src_dir_path = os.path.abspath(os.path.dirname(src_file_path))
        self.ip_dir_path = os.path.abspath(os.path.dirname(ip_file_path))
        self.container = None

    def run(self, scale, timeout):
        self.container = self.client.create_container(image='progeval:custom', network_disabled=True, 
            detach=True, command='evaluate %s' % scale, volumes=['/src/', '/ip/'], 
            host_config=self.client.create_host_config(binds={ 
                self.src_dir_path: {'bind': '/src/', 'mode': 'ro'},
                self.ip_dir_path: {'bind': '/ip/', 'mode': 'ro'},
            }, mem_limit='512m'))

        self.client.start(self.container)
        
        try:
            self.client.wait(self.container, timeout=timeout)
            logs = self.client.logs(self.container, stdout=True, stderr=True, tail='all', stream=True)
            return logs
        except ReadTimeout:
            self.client.remove_container(self.container, force=True)
            return None

    def close(self):
       self.client.remove_container(self.container) 

