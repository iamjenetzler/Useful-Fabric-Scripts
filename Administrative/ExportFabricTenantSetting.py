# This script will export the tenant settings to a CSV file and then save it to a Delta table in a Lakehouse.

from azure.identity import InteractiveBrowserCredential
import requests


import json, requests, pandas as pd
from datetime import date


TENANT_ID = ""

# Authenticate interactively
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
credential = InteractiveBrowserCredential()
token = credential.get_token(*SCOPE)

# Extract the access token
access_token = token.token
print("Access token acquired successfully!")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}


path = '/lakehouse/default/Files/TenantSettings/'
activityDate = date.today().strftime("%Y-%m-%d")

TenantSettingsURL = 'https://api.fabric.microsoft.com/v1/admin/tenantsettings'
TenantSettingsJSON = requests.get(TenantSettingsURL , headers=headers)

if TenantSettingsJSON.status_code != 200:
    print("Failed to retrieve tenant settings! {response.status_code}")
else:
    TenantSettingsJSONContent = json.loads(TenantSettingsJSON.text)
    TenantSettingsJSONContentExplode = TenantSettingsJSONContent['tenantSettings']
    print(TenantSettingsJSONContentExplode)

df = pd.DataFrame(TenantSettingsJSONContentExplode)
df['ExportedDate'] = activityDate
df.to_csv(path + activityDate + '_TenantSettings.csv', index=False) 

df = spark.read.format("csv").option("header","true").load("Files/TenantSettings/*.csv")
df.write.mode("overwrite").format("delta").saveAsTable("TenantSettings")
