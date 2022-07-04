# Export to elastic (JSON < 50MB)

Assign: Anonymous, Anonymous
Date Created: June 14, 2022 4:55 PM
Status: In Progress

We can break this down into 2 steps:

1. import a simple JSON from a file into the _bulk API through a simple POST curl command
2. Actually connect the Netflow generator to dump the JSON lines into the openSearch

lastly, we also need to define a mapping(template) for the JSON data, to make it easier to use afterwards

### using curl to dump a JSON directly into opensearch’s _bulk API

[https://opensearch.org/docs/latest/opensearch/rest-api/document-apis/bulk/](https://opensearch.org/docs/latest/opensearch/rest-api/document-apis/bulk/)

[https://stackoverflow.com/questions/61866140/python-automated-bulk-request-for-elasticsearch-not-working-must-be-terminated](https://stackoverflow.com/questions/61866140/python-automated-bulk-request-for-elasticsearch-not-working-must-be-terminated)

Remember to add 

```json
dd
```

, httpS, K flag to avoid cert check and login to get auth. 

JSON needs to be formatted correctly for it to be imported. There are flags for -d -data and --data-binary. Here’s an example of a newline delimited JSON(NDJSON) file that works:

[users.json](Export%20to%20elastic%20(JSON%2050MB)%201ad8e328b083468daa144a21cc97ea8f/users.json)

Notice the first line, it is required by nulk import to give the entry an index and a uid(?). 

```json
{"index": {"_index": "users", "_id": 1}}
{"fields": {"id": "5fe60ae52b40e53609c803ec","nom": "Jessica","prenom": "Herrera","aboutMe": "anim","socials": [{"name": "faacebook","url": "https://www.facebook.com/profile?id=5445546"},{"name": "linkedin","url": "https://www.linkedin.com/profile?id=5445546"}],"affiliations": [{"organisation": "ANARCO","equipe": "developpement","pays": "Russian Federation","dateD": "2013-06-03T00:00:00Z" ,"dateF": "2013-06-03T00:00:00Z" }]}}
```

```json
curl -k -X POST 'https://admin:admin@localhost:9200/_bulk?pretty' --data-binary @users.json -H 'Content-Type: application/json'
```

should return smt like

```json
{
  "took" : 40,
  "errors" : false,
  "items" : [
    {
      "index" : {
        "_index" : "users",
        "_id" : "1",
        "_version" : 2,
        "result" : "updated",
        "_shards" : {
          "total" : 2,
          "successful" : 2,
          "failed" : 0
        },
        "_seq_no" : 1,
        "_primary_term" : 1,
        "status" : 200
      }
    }
  ]
}
```

Now to check how it was parsed:

```json
~/D/B/python-netflow-v9-softflowd ❯❯❯ curl -k -X GET 'https://admin:admin@localhost:9200/users/_doc/1'                                                                                                     master ◼
{"_index":"users","_id":"1","_version":2,"_seq_no":1,"_primary_term":1,"found":true,"_source":{"fields": {"id": "5fe60ae52b40e53609c803ec","nom": "Jessica","prenom": "Herrera","aboutMe": "anim","socials": [{"name": "faacebook","url": "https://www.facebook.com/profile?id=5445546"},{"name": "linkedin","url": "https://www.linkedin.com/profile?id=5445546"}],"affiliations": [{"organisation": "ANARCO","equipe": "developpement","pays": "Russian Federation","dateD": "2013-06-03T00:00:00Z" ,"dateF": "2013-06-03T00:00:00Z" }]}}}⏎
```

- multi-line JSON can also be imported, example:

[multi_test.json](Export%20to%20elastic%20(JSON%2050MB)%201ad8e328b083468daa144a21cc97ea8f/multi_test.json)

### Actually doing it with a stream, instead of JSON files

There’s a OpenSearch lib for python that does most of the heavy lifting.

[open_exmp.py](Export%20to%20elastic%20(JSON%2050MB)%201ad8e328b083468daa144a21cc97ea8f/open_exmp.py)

 I did a small extension of the netflow python converter form above(”collector) to show how it would work, it opens a connection to a openSearch instance on default port, waits on port 6666 for netflows, converts them to json and submits to DB.

[collect_dump.py](Export%20to%20elastic%20(JSON%2050MB)%201ad8e328b083468daa144a21cc97ea8f/collect_dump.py)

Same applies as above, it has to involve a generator that creates flows (I used the same GO netflowGenerator from the other task. You might need to adjust either port number or ip in the script for it to work on your machine. If everything runs, you should be seeing:

```json
Adding json entry:
{'_index': 'python-test-index-1123', '_id': '1', '_version': 27, 'result': 'updated', 'forced_refresh': True, '_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_seq_no': 26, '_primary_term': 1}
```

Note the index name, you should change it to something like “netflow-v5-init” to make sure we all use the same index. 

### Resources:

1. Elastiflow KIBANA Dashboard from 2 yearsa go: [https://github.com/robcowart/elastiflow/blob/master/kibana/elastiflow.kibana.7.8.x.ndjson](https://github.com/robcowart/elastiflow/blob/master/kibana/elastiflow.kibana.7.8.x.ndjson)
2. New Elastiflow dashboards: [https://docs.elastiflow.com/docs/opensearch_dashboards](https://docs.elastiflow.com/docs/opensearch_dashboards)
3. Elastiflow Logstash template for JOSN import: [https://github.com/robcowart/elastiflow/blob/master/logstash/elastiflow/templates/elastiflow.template.json](https://github.com/robcowart/elastiflow/blob/master/logstash/elastiflow/templates/elastiflow.template.json)
4. CISCO blog netflowv5 Template: 

```json
curl -XPUT localhost:9200/_template/logstash_netflow5 -d '{
    "template" : "logstash_netflow5-*",
    "settings": {
      "index.refresh_interval": "5s"
    },
    "mappings" : {
      "_default_" : {
        "_all" : {"enabled" : false},
        "properties" : {
          "@version": { "index": "analyzed", "type": "integer" },
          "@timestamp": { "index": "analyzed", "type": "date" },
          "netflow": {
            "dynamic": true,
            "type": "object",
            "properties": {
              "version": { "index": "analyzed", "type": "integer" },
              "flow_seq_num": { "index": "not_analyzed", "type": "long" },
              "engine_type": { "index": "not_analyzed", "type": "integer" },
              "engine_id": { "index": "not_analyzed", "type": "integer" },
              "sampling_algorithm": { "index": "not_analyzed", "type": "integer" },
              "sampling_interval": { "index": "not_analyzed", "type": "integer" },
              "flow_records": { "index": "not_analyzed", "type": "integer" },
              "ipv4_src_addr": { "index": "analyzed", "type": "ip" },
              "ipv4_dst_addr": { "index": "analyzed", "type": "ip" },
              "ipv4_next_hop": { "index": "analyzed", "type": "ip" },
              "input_snmp": { "index": "not_analyzed", "type": "long" },
              "output_snmp": { "index": "not_analyzed", "type": "long" },
              "in_pkts": { "index": "analyzed", "type": "long" },
              "in_bytes": { "index": "analyzed", "type": "long" },
              "first_switched": { "index": "not_analyzed", "type": "date" },
              "last_switched": { "index": "not_analyzed", "type": "date" },
              "l4_src_port": { "index": "analyzed", "type": "long" },
              "l4_dst_port": { "index": "analyzed", "type": "long" }, 
              "tcp_flags": { "index": "analyzed", "type": "integer" },
              "protocol": { "index": "analyzed", "type": "integer" },
              "src_tos": { "index": "analyzed", "type": "integer" },
              "src_as": { "index": "analyzed", "type": "integer" },
              "dst_as": { "index": "analyzed", "type": "integer" },
              "src_mask": { "index": "analyzed", "type": "integer" },
              "dst_mask": { "index": "analyzed", "type": "integer" }
            }
          }
        }
      }
    }
  }'
```