Reference: https://dev.to/cosckoya/influxdb-v2-on-kubernetes-9eb

### Environment used: Minikube 

### Further Enhancements: 

### Collector.py 
- Time for each log entry is the same
- Update config to handle service name or host as ENV variable
- Unit testing
- Static code scanning

### Dockerfile
- Running as root user
- Not verifying dependencies
- image scanning

### InfluxDB
- Configurations for scale by limiting number of connections
- Store secrets in some secrets manager
- Change from StatefulSet to Deployment

### K8S
- Use external volumes
- Get logs visible from collector container to kubectl logs

### Conclusion:
The collector container isn't able to push up data while running as a deployment in k8s because it can't connect to the InfluxDB

### ERRORS 
- ERROR:influxdb_client.client.write_api:The batch item wasn't processed successfully because: Failed to parse: http://10.97.117.83:8086 # use servicename from env variable in k8s instead of fixed host:port/api/v2/write?org=InfluxData&bucket=kubernetes&precision=ns
- ERROR:influxdb_client.client.write_api:The batch item wasn't processed successfully because: HTTPConnectionPool(host='influxdb.local', port=8086): Max retries exceeded with url: /api/v2/write?org=InfluxData&bucket=kubernetes&precision=ns (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7fc918137640>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))# armis
