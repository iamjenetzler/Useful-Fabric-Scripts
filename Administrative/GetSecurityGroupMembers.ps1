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