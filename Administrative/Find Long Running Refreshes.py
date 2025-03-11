# This script will monitor all datasets in all workspaces and cancel any refreshes that have been running for longer than a specified timeout duration.
# The client needs to have access to all the workspaces to view dataset refreshes, so run AddAdminToWorkspaces.ps1 first.

import requests
import time
from datetime import datetime, timedelta

# Constants
TENANT_ID = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
POWER_BI_API_URL = "https://api.powerbi.com/v1.0/myorg/"
REFRESH_TIMEOUT_MINUTES = 60  # Set your timeout duration here (e.g., 60 minutes)


# Function to get an access token
def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://analysis.windows.net/powerbi/api/.default",
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# Function to get all workspaces
def get_workspaces(access_token):
    url = f"{POWER_BI_API_URL}groups"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

# Function to get datasets in a workspace
def get_datasets(access_token, group_id):
    url = f"{POWER_BI_API_URL}groups/{group_id}/datasets"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["value"]

# Function to get refresh history for a dataset
def get_refresh_history(access_token, group_id, dataset_id):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"  # Ensure this header is included
    }
    response = requests.get(url, headers=headers)  # No payload for GET request
    response.raise_for_status()  # Raise an error for HTTP issues
    print(response.text)

    return response.json()["value"]


# Function to cancel a refresh
def cancel_refresh(access_token, group_id, dataset_id, refresh_id):
    url = f"{POWER_BI_API_URL}groups/{group_id}/datasets/{dataset_id}/refreshes/{refresh_id}/cancel"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(f"Successfully canceled refresh for dataset {dataset_id}, refresh ID {refresh_id}.")
    else:
        print(f"Failed to cancel refresh for dataset {dataset_id}, refresh ID {refresh_id}: {response.text}")

# Main function to monitor and cancel long-running refreshes
def monitor_and_cancel_long_refreshes():
    access_token = get_access_token()
    workspaces = get_workspaces(access_token)
    now = datetime.utcnow()

    for workspace in workspaces:
        group_id = workspace["id"]
        datasets = get_datasets(access_token, group_id)

        for dataset in datasets:
            dataset_id = dataset["id"]
            refresh_history = get_refresh_history(access_token, group_id, dataset_id)

            for refresh in refresh_history:
                if refresh["status"] == "InProgress":
                    refresh_start_time = datetime.strptime(refresh["startTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    elapsed_time = now - refresh_start_time

                    if elapsed_time > timedelta(minutes=REFRESH_TIMEOUT_MINUTES):
                        print(f"Refresh for dataset {dataset_id} in workspace {group_id} has been running for {elapsed_time}. Cancelling...")
                        cancel_refresh(access_token, group_id, dataset_id, refresh["id"])

if __name__ == "__main__":
    monitor_and_cancel_long_refreshes()
