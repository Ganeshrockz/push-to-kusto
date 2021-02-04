import os
import json
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.ingest import KustoIngestClient, IngestionProperties, FileDescriptor, BlobDescriptor, DataFormat, ReportLevel, ReportMethod

import pprint
import time
from azure.kusto.ingest.status import KustoIngestStatusQueues
from datetime import datetime

def main():
    
    # Kusto cluster inputs
    data = os.environ["INPUT_DATA"]
    tenantId = os.environ["INPUT_TENANTID"]
    databaseName = os.environ["INPUT_DATABASE"]
    clusterName = os.environ["INPUT_CLUSTERNAME"]
    region = os.environ["INPUT_CLUSTERREGION"]
    clientId = os.environ["INPUT_CLIENTID"]
    clientSecret = os.environ["INPUT_CLIENTSECRET"]
    destinationTable = os.environ["INPUT_TABLE"]
    mapping = os.environ['INPUT_MAPPING']

    try:

        # file creation 

        #fileName = "sample.json"
        #filePath = os.path.join(os.environ["GITHUB_WORKSPACE"], fileName)

        deploymentData = {}
        deploymentData["Timestamp"] = str(datetime.now())
        deploymentData["DeploymentDetails"] = data

        #with open(filePath, "w") as targetFile:
         #   json.dump(deploymentData, targetFile)

        # cluster client connection and auth

        httpsPrefix = "https://"
        suffixKustoUri = "kusto.windows.net:443/"
        clusterIngestUri = "{0}ingest-{1}.{2}.{3}".format(httpsPrefix, clusterName, region, suffixKustoUri)

        kcsb_ingest = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                       clusterIngestUri, clientId, clientSecret, tenantId)

        print(mapping)

        # Cluster ingestion parameters
        ingestionClient = KustoIngestClient(kcsb_ingest)
        ingestionProperties = IngestionProperties(database=databaseName, table=destinationTable, dataFormat=DataFormat.JSON, ingestion_mapping_reference=mapping, report_level=ReportLevel.FailuresAndSuccesses)
        fileDescriptor = FileDescriptor(data, 1000)

        print('Payload to dump')
        with open(data, "r") as targetFile:
            parsed = json.load(targetFile)
            print(json.dumps(parsed, indent=2, sort_keys=True))

        ingestionClient.ingest_from_file(fileDescriptor, ingestion_properties=ingestionProperties)

        print('Queued up ingestion with Azure Data Explorer')

        # Remove the temporary file
        #os.remove(filePath)

        # Repeated pinging to wait for success/failure message
        qs = KustoIngestStatusQueues(ingestionClient)

        # Interval to ping
        MAX_BACKOFF = 5
        backoff = 1
        while True:
            if qs.success.is_empty() and qs.failure.is_empty():
                time.sleep(backoff)
                backoff = min(backoff * 2, MAX_BACKOFF)
                print("No new messages. backing off for {} seconds".format(backoff))
                continue

            backoff = 1

            success_messages = qs.success.pop(10)
            failure_messages = qs.failure.pop(10)

            pprint.pprint("SUCCESS : {}".format(success_messages))
            pprint.pprint("FAILURE : {}".format(failure_messages))
            break
    except Exception as e:
        raise Exception(e)


if __name__ == "__main__":
    main()
