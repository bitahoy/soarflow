yaml = helm(
  '.',
  name='soarflow',
  values=['./values.yaml']
  )
k8s_yaml(yaml)
k8s_resource(
    workload='soarflow-opensearch-dashboards',
    links=[
        link('https://opensearch.org/docs/latest/dashboards/index/', 'OpenSearch docs')
    ],
    port_forwards=[
        port_forward(5601, 5601, name='OpenSearch Dashboard')
    ])
k8s_resource(
    workload='opensearch-cluster-master',
    links=[
        link('https://opensearch.org/docs/latest/opensearch/index/', 'OpenSearch docs')
    ],
    port_forwards=[
        port_forward(9200, 9200, name='OpenSearch API (localhost:9200)')
    ])
docker_build('bitahoy/soarflow', 'soarflow')
k8s_resource(
    workload='soarflow-app',
    port_forwards=[
        port_forward(9300, 80, name='Soarflow Frontend (localhost:9300)')
    ])


local_resource('soarflow-main', cmd="pip3 install -r soarflow/requirements.txt", serve_cmd='python3 soarflow/src/main.py', deps=['soarflow/src/'], resource_deps=['opensearch-cluster-master', 'soarflow-opensearch-dashboards'])
local_resource('soarflow-bitahoycloud', cmd="pip3 install -r soarflow/requirements.txt", serve_cmd='python3 soarflow/src/bitahoycloud.py', deps=['soarflow/src/'], resource_deps=['opensearch-cluster-master', 'soarflow-opensearch-dashboards'])