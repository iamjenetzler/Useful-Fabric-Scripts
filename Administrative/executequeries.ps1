# This script executes a query against a Power BI dataset and returns the results. It requires the following parameters to be defined:

# Define the parameters
$tenantId = ''
$clientId = ''
$workspaceId = ''
$clientSecret = ''
$datasetId = ''
$url = "https://api.powerbi.com/v1.0/myorg/groups/$workspaceId/datasets/$datasetId/executeQueries"
$query = "EVALUATE TOPN(10, dimproduct)"

# Get the access token
$body = @{
    grant_type    = "client_credentials"
    client_id     = $clientId
    client_secret = $clientSecret
    resource      = "https://analysis.windows.net/powerbi/api"
}

$response = Invoke-RestMethod -Method Post -Uri "https://login.microsoftonline.com/$tenantId/oauth2/token" -ContentType "application/x-www-form-urlencoded" -Body $body
$accessToken = $response.access_token

# Execute the query
$headers = @{
    'Authorization' = "Bearer $accessToken"
    'Content-Type'  = 'application/json'
}

$body = @{
    queries = @(@{
        query = $query
    })
    serializerSettings = @{
        includeNulls = $true
    }
}

# Convert the body to JSON with a specified depth
$jsonBody = $body | ConvertTo-Json -Depth 10

# Log the JSON body for debugging
Write-Output "JSON Body: $jsonBody"

$response = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $jsonBody

# Log the response for debugging
Write-Output "Response: $response"

# Parse the response to extract the tables and rows
$results = $response.results
foreach ($result in $results) {
    $tables = $result.tables
    foreach ($table in $tables) {
        $rows = $table.rows
        foreach ($row in $rows) {
            Write-Output "Row: $row"
        }
    }
}