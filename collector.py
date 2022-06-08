import schedule
import time
import os
import socket
import logging

from influxdb_client import InfluxDBClient, Point, WriteOptions

BUCKET = "kubernetes" # influxDB bucket - retention policies
MEASUREMENT = "node_load" # database table
NODE_NAME = socket.gethostname() # database row index


def publish_node_load():
    """Read load averages for k8s node and publish to influx db
    :return: true on publish success, false otherwise

    Note: Could add :param: bucket to push to different buckets
    i.e. different clusters have different retention policies
    """
    # Get Load Metrics 
    current_time = time.time()
    load_1, load_5, load_15 = os.getloadavg()

    # Log Results
    log_string = str(current_time) + "|" + str(NODE_NAME) + "|" + str(load_1) + "|" + str(load_5) + "|" + str(load_15)
    print(log_string)
    logging.info(log_string)

    # Publish to InfluxDB
    # try: is this a nested try-catch block?
    
    ## Note: These are synchronous connections
    client = InfluxDBClient.from_config_file("config.ini")

    ## Note: Careful with retries, the writes are not asynced so this cannot take longer than 
    write_api = client.write_api(write_options=WriteOptions(retry_interval=1_000, # TODO: 2_000
                                                        max_retries=0, # TODO: 3
                                                        exponential_base=2))
                                                        

    ## Note: Less tags reduces cardinality
    # https://www.influxdata.com/blog/data-layout-and-schema-design-best-practices-for-influxdb/
    # https://stackoverflow.com/questions/58190272/what-are-series-and-bucket-in-influxdb
    p = Point(MEASUREMENT).tag("node", NODE_NAME).field("time", current_time).field("load_1", load_1).field("load_5", load_5).field("load_15", load_15)
    # Time is static

    write_api.write(bucket=BUCKET, record=p)
        
    '''
    except Error as e:
        error_str = "Publish to InfluxDB failed: ", e
        logger.Error(error_str)
        print(error_str)
        client.close()
        write_api.close()
        return False
    else:
        client.close()
        write_api.close()
        return True
    '''

    client.close()
    write_api.close()
    return True

# TODO: Write log to external file or perform cleanup on regular (daily) interval
logging.basicConfig(filename='collector.log', level=logging.DEBUG)

# schedule.every(1).minutes.do(publish_node_load) // TODO
schedule.every(1).seconds.do(publish_node_load)

while True:
    schedule.run_pending()
    time.sleep(1)