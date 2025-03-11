# This script retrieves and exports the members of all security groups in Azure Active Directory to a CSV file. It requires the Microsoft.Graph module to be installed and connected to Azure Active Directory.

# Install-Module Microsoft.Graph -Scope CurrentUser
# Connect-MgGraph -Scopes "Group.Read.All"

# Get all security groups
$groups = Get-MgGroup -All | Where-Object {$_.SecurityEnabled -eq $true}

# Initialize an array to store group members
$groupMembers = @()

# Loop through each group to get its members
foreach ($group in $groups) {
    $members = Get-MgGroupMemberAsUser -GroupId $group.Id -All
    foreach ($member in $members) {
        $groupMembers += [PSCustomObject]@{
            GroupName = $group.DisplayName
            MemberName = $member.Mail
           
             
        }
    }
}

# Export the results to a CSV file
 $groupMembers | Export-Csv -Path "C:\Users\jeetzler\OneDrive - Microsoft\Customer Engagements\Disney\Disney - Robert Strong PBI\GroupMembers.csv" -NoTypeInformation