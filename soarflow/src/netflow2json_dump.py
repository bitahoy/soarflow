import argparse
import gzip
import json
import logging
import time
logger = logging.getLogger()

# https://github.com/bitkeks/python-netflow-v9-softflowd
from netflow.collector import get_export_packets
# opensearch python lib
from opensearchpy import OpenSearch, exceptions


def connect_opensearch(index_name_var):
    host = 'localhost'
    port = 9200
    auth = ('admin', 'admin')  # For testing only. Don't store credentials in code.
    ca_certs_path = '/full/path/to/root-ca.pem'  # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Optional client certificates if you don't want to use HTTP basic authentication.
    # client_cert_path = '/full/path/to/client.pem'
    # client_key_path = '/full/path/to/client-key.pem'

    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    print('\Settings-up client to connect to OpenSearch....')
    opensearch_client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        ca_certs=ca_certs_path
    )

    # Create an index with non-default settings.
    index_name = index_name_var
    index_body = {
        'settings': {
            'index': {
                'number_of_shards': 4
            }
        }
    }
    # index_body = {
    #     'settings': {
    #         'index': {
    #             'number_of_shards': 4
    #         }
    #     },
    #     "mappings": {
    #         "_default_": {
    #             "_all": {
    #                 "enabled": False
    #             },
    #             "properties": {
    #                 "@version": {
    #                     "index": "analyzed",
    #                     "type": "integer"
    #                 },
    #                 "@timestamp": {
    #                     "index": "analyzed",
    #                     "type": "date"
    #                 },
    #                 "netflow": {
    #                     "dynamic": True,
    #                     "type": "object",
    #                     "properties": {
    #                         "version": {
    #                             "index": "analyzed",
    #                             "type": "integer"
    #                         },
    #                         "flow_seq_num": {
    #                             "index": "not_analyzed",
    #                             "type": "long"
    #                         },
    #                         "engine_type": {
    #                             "index": "not_analyzed",
    #                             "type": "integer"
    #                         }
    #                         }
    #                 }
    #             }
    #         }
    #     }
    # }


    try:
        # opensearch_client.indices.create(index)
        response = opensearch_client.indices.create(index_name, body=index_body)
        print('\nCreating index:')
        print(response)
    except exceptions.RequestError as ex:
        if ex.error == 'resource_already_exists_exception':
            print("\nindex_already_exists so we don't add it again")
            pass  # Index already exists. Ignore.
        else:  # Other exception - raise it
            raise ex

    return opensearch_client


def remve_entries_clean_index(index_name, submitted_ids):
    # iterate over the ids that we submitted and delete each one
    for id in submitted_ids:
        # Delete the document.
        response = opensearch_client.delete(
            index=index_name,
            id=id
        )

        print('\nDeleting document:')
        print(response)

    # Delete the index.
    response = opensearch_client.indices.delete(
        index=index_name
    )

    print('\nDeleting index:')
    print(response)


def sumbit_json(opensearch_client, index_name_var, id, json_entry):
    # Add a document to the index.
    dummy_json_entry = {"1655817798.8633146": {"client": ['172.30.37.246', '47524'],
                                               "header": {"version": 5, "count": 16, "uptime": 1000,
                                                          "timestamp": 1655817798, "timestamp_nano": 862798141,
                                                          "sequence": 1, "engine_type": 1, "engine_id": 0,
                                                          "sampling_interval": 0},
                                               "flows": [{"IPV4_SRC_ADDR": 1879708682, "IPV4_DST_ADDR": 2887695882, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0,
             "IN_PACKETS": 921, "IN_OCTETS": 919, "FIRST_SWITCHED": 389, "LAST_SWITCHED": 628, "SRC_PORT": 40,
             "DST_PORT": 80, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 19666, "DST_AS": 52270, "SRC_MASK": 3,
             "DST_MASK": 12},
            {"IPV4_SRC_ADDR": 3232240650, "IPV4_DST_ADDR": 3389832714, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0,
             "IN_PACKETS": 452, "IN_OCTETS": 13, "FIRST_SWITCHED": 702, "LAST_SWITCHED": 910, "SRC_PORT": 40,
             "DST_PORT": 443, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 59455, "DST_AS": 45777, "SRC_MASK": 8,
             "DST_MASK": 26}]}}
    # id = '1' #id
    # sample code from https://opensearch.org/docs/latest/clients/python
    response = opensearch_client.index(
        index=index_name_var,
        body=json_entry,
        # body = json.dumps(json_entry),
        id=str(id).replace('.', ''),  # Opensearch doesn't accept commas in id names.,  # we use timestamp (ts_ from the function above on the stack)
        refresh=True
    )

    print('\nAdding json entry:')
    print(response)

def write_to_file(ts, entry):
    ## old write-t-file function
    entry = {ts: entry}
    line = json.dumps(entry).encode() + b"\n"  # byte encoded line
    with gzip.open(args.output_file, "ab") as fh:  # open as append, not reading the whole file
        fh.write(line)

# def manually_json_import():
#     ## old write-t-file function
#     entry = {ts: entry}
#     line = json.dumps(entry).encode() + b"\n"  # byte encoded line
#     with gzip.open(args.output_file, "ab") as fh:  # open as append, not reading the whole file
#         fh.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collector that formats to JSON and dumps into openSearch API")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="collector listening address")
    parser.add_argument("--port", "-p", type=int, default=6666,
                        help="collector listener port")
    parser.add_argument("--file", "-o", type=str, dest="output_file",
                        default="{}.gz".format(int(time.time())),
                        help="collector export multiline JSON file")
    parser.add_argument("--debug", "-D", action="store_true",
                        help="Enable debug output")
    args = parser.parse_args()

    index_name_var = 'netflow-v9-' + '001' #roman_netflow5-*
    opensearch_client = connect_opensearch(index_name_var)
    submitted_ids = []  # used for testing to keep track how many entries are added to delete them afterwards

    if args.debug:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    try:
        # With every parsed flow a new line is appended to the output file. In previous versions, this was implemented
        # by storing the whole data dict in memory and dumping it regularly onto disk. This was extremely fragile, as
        # it a) consumed a lot of memory and CPU (dropping packets since storing one flow took longer than the arrival
        # of the next flow) and b) broke the exported JSON file, if the collector crashed during the write process,
        # rendering all collected flows during the runtime of the collector useless (the file contained one large JSON
        # dict which represented the 'data' dict).

        # In this new approach, each received flow is parsed as usual, but it gets appended to a gzipped file each time.
        # All in all, this improves in three aspects:
        # 1. collected flow data is not stored in memory any more
        # 2. received and parsed flows are persisted reliably
        # 3. the disk usage of files with JSON and its full strings as keys is reduced by using gzipped files
        # This also means that the files have to be handled differently, because they are gzipped and not formatted as
        # one single big JSON dump, but rather many little JSON dumps, separated by line breaks.
        for ts, client, export in get_export_packets(args.host, args.port):
            entry = {
                "client": [str(i) for i in client],  # gotta cast to str or else it fails on sumbission to Opensearch
                "header": export.header.to_dict(),
                "flows": [flow.data for flow in export.flows]
            }
            # print whole josn to std
            print(json.dumps(entry, indent=4, sort_keys=True))
            # print only ts for logging
            # print(ts)
            submitted_ids.append(ts)  # used as uids
            sumbit_json(opensearch_client, index_name_var, ts, entry)
            # write_to_file(ts, entry)

    except KeyboardInterrupt:
        remove_entires= False
        if (remove_entires):
            remve_entries_clean_index(opensearch_client, index_name_var, submitted_ids)
        logger.info("Received KeyboardInterrupt, passing through")
        pass
