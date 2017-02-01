curl -XPOST 'localhost:9200/incoming-sensors/_update_by_query' -d '
{
  "script": {
    "inline": "ctx._source.customer = \"Chess\""
  },
  "query": {
    "bool": {
        "must_not": {
            "exists": {
                "field": "customer"
                }
            }

        }
    }
}'
