# SOARFlow

# Context: Hackathon in cooperation with the Cybersecurity day 2022

This software was created to solve a challenge of the Hackathon which was provided by saarLB. The goal of this challenge is to create a configurable and adjustable dashboard which is able to include/import data using different information sources.

Requirements:

- It should be possible to create views for different stakeholders (board member, security management, IT staff)
- The result should be easily adaptable to all kind of input data originating from log servers, APIs, databases, key-value-stores, ...
- You can use already existing open source tools (e.g. grafana) or apps/services in the Microsoft cloud

## Our solution

We took OpenSearch as the foundation to solve this problem. OpenSearch is an open source search engine and dashboard. It can be used to store data and visualize it in different dashboards for different stakeholders. In our solution, we used a helm chart to make it easy to spin up an OpenSearch instance in a kubernetes cluster. For local development, Tilt is used. In combination, we can run OpenSearch and the rest of this project fromk the commandline just by executing `tilt up`.

To get data into OpenSearch, we created some scripts and also a useful web dashboard to upload various file formats. The supported file formats are: CSV, PCAP and JSON. This can be generated data or hand-crafted data.

Also, we created pipelines for netflow data and data from Bitahoy's Cloud API to showcase the possibility to stream all kinds of data into OpenSearch through our code.

In various dashboards, we created a few charts to visualize the data.

### Technologies used

- Tilt: A tool for local development
- Helm: A tool for deploying charts to kubernetes
- OpenSearch: A search engine and dashboard
- OpenSearch-Dashboard: A web dashboard for OpenSearch
- python-fastapi: A REST API framework for Python
- python-asyncio: A library for asynchronous programming in Python
- python-aiohttp: A library for making HTTP requests in Python
- scapy: A library for packet parsing and crafting
- ...


# Screenshots

![](/screenshots/1.png)
![](/screenshots/2.png)
![](/screenshots/3.png)
![](/screenshots/4.jpg)


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