curl -XPOST 'localhost:9200/incoming-sensors/_search?size=1000&pretty=1' -d '
{
  "query": {
    "match": {
      "sensor_name": "T1"
    }
  }
}'
