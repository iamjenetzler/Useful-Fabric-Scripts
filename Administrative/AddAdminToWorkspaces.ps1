# This script adds a user or service principal as an admin to all workspaces in Power BI.

param (
    # This can add a user by email address or a security principal   
    # If providing a security principal, this is the Objec Id of the Enterprise Application
    [string]$PrincipalOrUser =  'a3e87864-ca1a-443c-8e41-bec46625310e',    
    [string]$Folder = "out"
)

# Authenticate to Power BI using an admin account
try {
    Write-Host "Please log in with your admin account to connect to Power BI..."
    Connect-PowerBIServiceAccount
    Write-Host "Connected to Power BI Service Account successfully."
} catch {
    Write-Host "Error connecting to Power BI Service Account: $_"
    throw
}

# Determine if the input is a service principal or user email
$isServicePrincipal = $PrincipalOrUser -match "^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$" # GUID format
if ($isServicePrincipal) {
    $PrincipalType = "App" # Correct value for service principals
    Write-Host "Input is identified as a Service Principal: $PrincipalOrUser"
} else {
    $PrincipalType = "User" # Correct value for user emails
    Write-Host "Input is identified as a User Email: $PrincipalOrUser"
}


# Loop through all workspaces
$Groups | ForEach-Object {
    Write-Host "Processing workspace: $($_.Name) (ID: $($_.Id))"

    # Flag to check if the user or service principal already exists
    $UserExists = $false

    # Loop through all users in the workspace
    foreach ($User in $_.Users) {
        Write-Host "Checking user: $($User.Identifier) with access right: $($User.AccessRight)"

        # Check if the current user matches the PrincipalOrUser
        if ($User.Identifier -eq $PrincipalOrUser) {
            Write-Host "$PrincipalOrUser already exists in the workspace with access right: $($User.AccessRight)"
            $UserExists = $true
            break
        }
    }

    # If the user or service principal does not exist, add them as an admin
    if (-not $UserExists) {
        Write-Host "Adding $PrincipalOrUser as administrator of the workspace: $($_.Name) (ID: $($_.Id))"
        try {
            Add-PowerBIWorkspaceUser -Scope Organization -Id $_.Id -Identifier $PrincipalOrUser -PrincipalType $PrincipalType -AccessRight Admin -WarningAction Ignore
            Write-Host "$PrincipalOrUser added successfully as an administrator."
        } catch {
            Write-Host "Error adding $PrincipalOrUser to workspace $($_.Name) (ID: $($_.Id)): $($_.Exception.Message)"
        }
    }
}


# Disconnect from Power BI
try {
    Disconnect-PowerBIServiceAccount
    Write-Host "Disconnected from Power BI Service Account."
} catch {
    Write-Host "Error disconnecting from Power BI Service Account: $_"
    throw
}
