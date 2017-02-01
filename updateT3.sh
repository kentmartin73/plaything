curl -XPOST 'localhost:9200/incoming-sensors/_update_by_query' -d '
{
  "script": {
    "inline": "ctx._source.sensor_name = \"Central heating return\""
  },
  "query": {
    "match": {
      "sensor_name": "T3"
    }
  }
}'
