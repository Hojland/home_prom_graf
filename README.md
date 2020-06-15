# home_prom_graf
Prometheus + Grafana stack built with data from micro:bit with attached envirobit sensors (bme280 environment, tcs3472 colour and mems microphone) and external sources


TODO:
- [] Set up Grafana and save templates
- [] Make PromQL query to make heatmap or mean over the hours
- [] Make extra info om mean temp in this hour and that hour etc..
- [] Make elastic unique ID (datetime)
- [] Make tester to see if new data is already indexed
- [] Make it runs once every hour
- [] Set up serverless
- [] Make sure it runs free

{"search_type":"query_then_fetch","ignore_unavailable":true,"index":"wattage"}
{"size":0,"query":{"bool":{"filter":[{"range":{"datetime":{"gte":"1583014020944","lte":"1583618820944","format":"epoch_millis"}}},{"query_string":{"analyze_wildcard":true,"query":"*"}}]}},"aggs":{"2":{"terms":{"field":"hour","size":20,"order":{"_key":"desc"},"min_doc_count":1},"aggs":{"1":{"avg":{"field":"quantity"}}}}}}

maybe check time
and where this it say groupby?
size=0?
url=http://192.168.0.10:3000/api/datasources/proxy/4/_msearch?max_concurrent_shard_requests=5
aggs 1 and 2?