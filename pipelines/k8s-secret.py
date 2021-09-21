from kubernetes import client, config
config.load_incluster_config()
v1=client.CoreV1Api()

print(v1.read_namespaced_secret("aws2", "singhr68"))
