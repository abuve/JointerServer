from django.test import TestCase

# Create your tests here.

import docker

# client = docker.from_env()
client = docker.DockerClient(base_url='tcp://10.167.11.118:2375')
clt = docker.APIClient(base_url='tcp://10.167.11.118:2375')

# li = clt.stats('1fdd3381ab06', stream=True)
#
# for i in li:
#     print(i)


for event in client.containers.list(limit=1):
    print(event.id)
    print(event.name)
    print(event.stats(stream=False))



#print(client.containers.list())