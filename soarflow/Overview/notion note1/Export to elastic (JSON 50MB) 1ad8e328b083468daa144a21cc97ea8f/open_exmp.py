from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
# client_cert_path = '/full/path/to/client.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    # client_cert = client_cert_path,
    # client_key = client_key_path,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)

# Create an index with non-default settings.
index_name = 'python-test-index2'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index_name, body=index_body)
print('\nCreating index:')
print(response)

# Add a document to the index.
document = {"1655817798.8633146": {"client": ["172.30.37.246", "47524"], "header": {"version": 5, "count": 16, "uptime": 1000, "timestamp": 1655817798, "timestamp_nano": 862798141, "sequence": 1, "engine_type": 1, "engine_id": 0, "sampling_interval": 0}, "flows": [{"IPV4_SRC_ADDR": 1879708682, "IPV4_DST_ADDR": 2887695882, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 921, "IN_OCTETS": 919, "FIRST_SWITCHED": 389, "LAST_SWITCHED": 628, "SRC_PORT": 40, "DST_PORT": 80, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 19666, "DST_AS": 52270, "SRC_MASK": 3, "DST_MASK": 12}, {"IPV4_SRC_ADDR": 3232240650, "IPV4_DST_ADDR": 3389832714, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 452, "IN_OCTETS": 13, "FIRST_SWITCHED": 702, "LAST_SWITCHED": 910, "SRC_PORT": 40, "DST_PORT": 443, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 59455, "DST_AS": 45777, "SRC_MASK": 8, "DST_MASK": 26}, {"IPV4_SRC_ADDR": 168432762, "IPV4_DST_ADDR": 1410121426, "NEXT_HOP": 3234270977, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 956, "IN_OCTETS": 770, "FIRST_SWITCHED": 652, "LAST_SWITCHED": 734, "SRC_PORT": 12001, "DST_PORT": 8080, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 25689, "DST_AS": 61059, "SRC_MASK": 5, "DST_MASK": 8}, {"IPV4_SRC_ADDR": 1004314234, "IPV4_DST_ADDR": 168618450, "NEXT_HOP": 667356929, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 449, "IN_OCTETS": 749, "FIRST_SWITCHED": 391, "LAST_SWITCHED": 674, "SRC_PORT": 9221, "DST_PORT": 53, "TCP_FLAGS": 0, "PROTO": 17, "TOS": 0, "SRC_AS": 21465, "DST_AS": 49400, "SRC_MASK": 12, "DST_MASK": 5}, {"IPV4_SRC_ADDR": 2886742538, "IPV4_DST_ADDR": 2215412234, "NEXT_HOP": 2215412225, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 237, "IN_OCTETS": 87, "FIRST_SWITCHED": 191, "LAST_SWITCHED": 572, "SRC_PORT": 0, "DST_PORT": 0, "TCP_FLAGS": 0, "PROTO": 1, "TOS": 0, "SRC_AS": 41905, "DST_AS": 7316, "SRC_MASK": 4, "DST_MASK": 31}, {"IPV4_SRC_ADDR": 4150793418, "IPV4_DST_ADDR": 168607242, "NEXT_HOP": 3234270977, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 11, "IN_OCTETS": 10, "FIRST_SWITCHED": 691, "LAST_SWITCHED": 822, "SRC_PORT": 40, "DST_PORT": 123, "TCP_FLAGS": 0, "PROTO": 17, "TOS": 0, "SRC_AS": 57632, "DST_AS": 30718, "SRC_MASK": 32, "DST_MASK": 8}, {"IPV4_SRC_ADDR": 2887652454, "IPV4_DST_ADDR": 1041022474, "NEXT_HOP": 2210860801, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 395, "IN_OCTETS": 183, "FIRST_SWITCHED": 787, "LAST_SWITCHED": 938, "SRC_PORT": 9010, "DST_PORT": 993, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 5437, "DST_AS": 36838, "SRC_MASK": 12, "DST_MASK": 5}, {"IPV4_SRC_ADDR": 177869836, "IPV4_DST_ADDR": 1292680798, "NEXT_HOP": 2517930241, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 795, "IN_OCTETS": 688, "FIRST_SWITCHED": 470, "LAST_SWITCHED": 619, "SRC_PORT": 9010, "DST_PORT": 3306, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 4211, "DST_AS": 11312, "SRC_MASK": 28, "DST_MASK": 17}, {"IPV4_SRC_ADDR": 477686558, "IPV4_DST_ADDR": 3747799804, "NEXT_HOP": 2094369731, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 469, "IN_OCTETS": 814, "FIRST_SWITCHED": 551, "LAST_SWITCHED": 944, "SRC_PORT": 47094, "DST_PORT": 21285, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 18683, "DST_AS": 39762, "SRC_MASK": 25, "DST_MASK": 17}, {"IPV4_SRC_ADDR": 2887652454, "IPV4_DST_ADDR": 3725377034, "NEXT_HOP": 3234270977, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 229, "IN_OCTETS": 914, "FIRST_SWITCHED": 213, "LAST_SWITCHED": 587, "SRC_PORT": 40, "DST_PORT": 22, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 31285, "DST_AS": 48651, "SRC_MASK": 29, "DST_MASK": 30}, {"IPV4_SRC_ADDR": 4150793418, "IPV4_DST_ADDR": 168607242, "NEXT_HOP": 3234270977, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 452, "IN_OCTETS": 829, "FIRST_SWITCHED": 777, "LAST_SWITCHED": 910, "SRC_PORT": 40, "DST_PORT": 6681, "TCP_FLAGS": 0, "PROTO": 17, "TOS": 0, "SRC_AS": 25066, "DST_AS": 50893, "SRC_MASK": 32, "DST_MASK": 29}, {"IPV4_SRC_ADDR": 3232240842, "IPV4_DST_ADDR": 705478154, "NEXT_HOP": 3234270977, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 93, "IN_OCTETS": 675, "FIRST_SWITCHED": 304, "LAST_SWITCHED": 692, "SRC_PORT": 40, "DST_PORT": 6682, "TCP_FLAGS": 0, "PROTO": 17, "TOS": 0, "SRC_AS": 3677, "DST_AS": 63079, "SRC_MASK": 32, "DST_MASK": 4}, {"IPV4_SRC_ADDR": 1879729162, "IPV4_DST_ADDR": 3232266250, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 987, "IN_OCTETS": 272, "FIRST_SWITCHED": 609, "LAST_SWITCHED": 886, "SRC_PORT": 40, "DST_PORT": 21, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 23676, "DST_AS": 13370, "SRC_MASK": 18, "DST_MASK": 14}, {"IPV4_SRC_ADDR": 1879708682, "IPV4_DST_ADDR": 2887695882, "NEXT_HOP": 2898726657, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 100, "IN_OCTETS": 55, "FIRST_SWITCHED": 298, "LAST_SWITCHED": 743, "SRC_PORT": 40, "DST_PORT": 161, "TCP_FLAGS": 0, "PROTO": 17, "TOS": 0, "SRC_AS": 23742, "DST_AS": 2695, "SRC_MASK": 20, "DST_MASK": 16}, {"IPV4_SRC_ADDR": 2886742538, "IPV4_DST_ADDR": 2215412234, "NEXT_HOP": 2215412225, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 208, "IN_OCTETS": 199, "FIRST_SWITCHED": 831, "LAST_SWITCHED": 967, "SRC_PORT": 0, "DST_PORT": 0, "TCP_FLAGS": 0, "PROTO": 1, "TOS": 0, "SRC_AS": 64813, "DST_AS": 1626, "SRC_MASK": 28, "DST_MASK": 9}, {"IPV4_SRC_ADDR": 821536269, "IPV4_DST_ADDR": 3251796204, "NEXT_HOP": 2445692703, "INPUT": 0, "OUTPUT": 0, "IN_PACKETS": 692, "IN_OCTETS": 852, "FIRST_SWITCHED": 484, "LAST_SWITCHED": 954, "SRC_PORT": 53968, "DST_PORT": 55505, "TCP_FLAGS": 0, "PROTO": 6, "TOS": 0, "SRC_AS": 32663, "DST_AS": 12296, "SRC_MASK": 0, "DST_MASK": 13}]}}
id = '2'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print('\nAdding document:')
print(response)

# # Search for the document.
# q = 'miller'
# query = {
#   'size': 5,
#   'query': {
#     'multi_match': {
#       'query': q,
#       'fields': ['title^2', 'director']
#     }
#   }
# }
#
# response = client.search(
#     body = query,
#     index = index_name
# )
# print('\nSearch results:')
# print(response)

# Delete the document.
response = client.delete(
    index = index_name,
    id = id
)

print('\nDeleting document:')
print(response)

# Delete the index.
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)
