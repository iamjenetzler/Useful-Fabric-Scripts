import requests

# Define the API endpoint and access token
api_endpoint = "https://api.powerbi.com/v1.0/myorg/groups"
access_token = "<your_access_token>"

# Function to get all workspaces
def get_workspaces():
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(api_endpoint, headers=headers)
    return response.json()

# Function to get datasets in a workspace
def get_datasets(group_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{api_endpoint}/{group_id}/datasets", headers=headers)
    return response.json()

# Function to check dataset properties
def check_dataset_properties(group_id, dataset_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"{api_endpoint}/{group_id}/datasets/{dataset_id}", headers=headers)
    return response.json()

# Main script
workspaces = get_workspaces()
for workspace in workspaces['value']:
    group_id = workspace['id']
    datasets = get_datasets(group_id)
    for dataset in datasets['value']:
        dataset_id = dataset['id']
        properties = check_dataset_properties(group_id, dataset_id)
        if properties.get('storageMode') == 'PremiumFiles' and properties.get('isLargeStorageFormat'):
            print(f"Workspace: {workspace['name']}, Dataset: {dataset['name']} is a large semantic model.")