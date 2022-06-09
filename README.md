# SOARFlow

# Setup

## Known issues

### max_map_count too low

If opensearch refuses to start and you see this error messege:

```
Max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

Then, run this command on your shell:

```
sysctl -w vm.max_map_count=262144
```

Might have to redo this after every restart. For permanent fix, add `vm.max_map_count = 262144` to `/etc/sysctl.conf`

Source: [good old stackoverflow, what else?](https://stackoverflow.com/questions/51445846/elasticsearch-max-virtual-memory-areas-vm-max-map-count-65530-is-too-low-inc) or [OpenSearch docs](https://opensearch.org/docs/latest/opensearch/install/important-settings/)


### Default configuration is insecure

The default configuration is insecure and should not be deployed in production. Default credentials: `admin:admin`


## Tilt

Tilt is a good way to debug a set of docker-containers locally in a minimal kubernetes cluster and solves almost all works-for-me issues. Something like docker-compose but in cool. Also has features to rebuild containers automagically whenever you make changes to the code.

[Video: Tilt in 2 minutes](https://youtu.be/FSMc3kQgd5Y)
[Website](https://tilt.dev/)

### Setup Tilt

Dependencies:

- Docker
- Tilt
```
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | sudo bash
```
- Helm
```
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```
- ctlptl
```
CTLPTL_VERSION="0.5.0"
curl -fsSL https://github.com/tilt-dev/ctlptl/releases/download/v$CTLPTL_VERSION/ctlptl.$CTLPTL_VERSION.linux.x86_64.tar.gz | sudo tar -xzv -C /usr/local/bin ctlptl
```
- [kubectl](https://kubernetes.io/de/docs/tasks/tools/install-kubectl/)

- Kind (or any other local kubernetes cluster)
```
# install go
sudo apt-get install golang-go
# install kind
go get sigs.k8s.io/kind
# fix path
sudo ln -s $(go env GOPATH)/bin/kind /usr/bin/kind
# create cluster
sudo -s ctlptl create cluster kind --registry=ctlptl-registry
sudo ctlptl get cluster kind-kind -o template --template '{{.status.localRegistryHosting.host}}'
```



### Use Tilt

```
cd opensearch
sudo helm dep update
cd ..
sudo helm dep update
sudo tilt up
```
To delete all resources again:
```
sudo tilt down
```