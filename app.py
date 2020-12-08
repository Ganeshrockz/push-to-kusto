import os
import json
#from azure.storage.blob import BlockBlobService, PublicAccess
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.kusto.ingest import KustoIngestClient, IngestionProperties, FileDescriptor, BlobDescriptor, DataFormat, ReportLevel, ReportMethod

def main():
    # Blob inputs
    storageAccountName = os.environ["INPUT_STORAGEACCOUNT"]
    storageAccountKey = os.environ["INPUT_STORAGEACCOUNTKEY"]
    containerName = os.environ["INPUT_CONTAINER"]
    
    # Kusto cluster inputs
    tenantId = os.environ["INPUT_TENANTID"]
    databaseName = os.environ["INPUT_DATABASE"]
    clusterName = os.environ["INPUT_CLUSTERNAME"]
    region = os.environ["INPUT_CLUSTERREGION"]
    clientId = os.environ["INPUT_CLIENTID"]
    clientSecret = os.environ["INPUT_CLIENTSECRET"]
    destinationTable = os.environ["INPUT_TABLE"]

    try:
        # Create blob client
        #blob_service_client = BlockBlobService(
         #   account_name=storageAccountName, account_key=storageAccountKey)

        fileName = "sample.json"
        filePath = os.path.join(os.environ["GITHUB_WORKSPACE"], fileName)

        deploymentData = {}
        deploymentData["Id"] = 3
        deploymentData["DeploymentDetails"] = "{\"clustername\":\"aks-sample\"}"

        with open(filePath, "w") as targetFile:
            json.dump(deploymentData, targetFile)

        #blob_service_client.create_blob_from_path(
        #    containerName, fileName, filePath)
        
        #print("Uploaded to blob storage")

        # Blob creation finished

        # Push blob to kusto

        httpsPrefix = "https://"
        suffixKustoUri = "kusto.windows.net:443/"
        clusterUri = "{0}{1}.{2}.{3}".format(httpsPrefix, clusterName, region, suffixKustoUri)
        clusterIngestUri = "{0}ingest-{1}.{2}.{3}".format(httpsPrefix, clusterName, region, suffixKustoUri)

        kcsb_ingest = KustoConnectionStringBuilder.with_aad_application_key_authentication(
                       clusterIngestUri, clientId, clientSecret, tenantId)

        #blobUri = "https://{0}.blob.core.windows.net/{1}/{2}".format(storageAccountName, containerName, fileName)

        ingestionClient = KustoIngestClient(kcsb_ingest)
        ingestionProperties = IngestionProperties(database=databaseName, table=destinationTable, dataFormat=DataFormat.JSON)
        fileDescriptor = FileDescriptor(filePath)
        
        print(filePath)

        with open(filePath, "r") as targetFile:
            parsed = json.load(deploymentData, targetFile)
            print(json.dumps(parsed, indent=2, sort_keys=True))

        ingestionClient.ingest_from_file(fileDescriptor, ingestion_properties=ingestionProperties)

        print('Done queuing up ingestion with Azure Data Explorer')
        os.remove(filePath)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()