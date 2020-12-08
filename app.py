import os
import json
from azure.storage.blob import BlockBlobService, PublicAccess

def main():
    # Create blob client

    storageAccountName = os.environ["INPUT_STORAGEACCOUNT"]
    storageAccountKey = os.environ["INPUT_STORAGEACCOUNTKEY"]
    containerName = os.environ["INPUT_CONTAINER"]

    try:
        blob_service_client = BlockBlobService(
            account_name=storageAccountName, account_key=storageAccountKey)

        fileName = "sample.json"
        filePath = os.path.join(os.environ["GITHUB_WORKSPACE"], fileName)

        deploymentData = {}
        deploymentData["Id"] = 3
        deploymentData["DeploymentDetails"] = "{\"clustername\":\"aks-sample\"}"

        with open(filePath, "w") as targetFile:
            json.dump(deploymentData, targetFile)

        blob_service_client.create_blob_from_path(
            containerName, fileName, filePath)
        
        print("Uploaded to blob storage")
        
        os.remove(filePath)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()