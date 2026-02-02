# ------------------------------
# MoMo API Full CRUD Test Script
# Automatically uses the ID returned by POST
# ------------------------------

# 1️ Set credentials
$pair = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:password123"))
$headers = @{ Authorization = ("Basic {0}" -f $pair) }

# 2️ Function to pretty print results
function Show-Result($title, $result) {
    Write-Host "===== $title ====="
    $result | ConvertTo-Json -Depth 5
    Write-Host "`n"
}

# 3️ GET all transactions (before POST)
$allBefore = Invoke-RestMethod -Uri "http://localhost:8500/transactions" -Headers $headers
Show-Result "All Transactions Before POST" $allBefore

# 4️ POST a new transaction
$newTransaction = @{
    transactionType = "1"
    amount = 5000
    sender = "M-Money"
    receiver = "Alice Smith"
    body = "TxId: custom12345. Your payment of 5000 RWF to Alice Smith..."
} | ConvertTo-Json

$postResponse = Invoke-RestMethod -Uri "http://localhost:8500/transactions" -Method POST -Headers $headers -Body $newTransaction -ContentType "application/json"
Show-Result "POST Response (New Transaction)" $postResponse

# 5️ Extract the short ID automatically
$shortId = $postResponse.id

# 6️ GET the new transaction
$getResponse = Invoke-RestMethod -Uri "http://localhost:8500/transactions/$shortId" -Headers $headers
Show-Result "GET Response (New Transaction by ID)" $getResponse

# 7️ UPDATE the transaction (PUT)
$updateData = @{
    amount = 5500
    receiver = "Gasasira"
    body = "TxId: custom12345. Your payment of 5500 RWF to Gasasira..."
} | ConvertTo-Json

$putResponse = Invoke-RestMethod -Uri "http://localhost:8500/transactions/$shortId" -Method PUT -Headers $headers -Body $updateData -ContentType "application/json"
Show-Result "PUT Response (Updated Transaction)" $putResponse

# 8️ DELETE the transaction
$deleteResponse = Invoke-RestMethod -Uri "http://localhost:8500/transactions/$shortId" -Method DELETE -Headers $headers
Show-Result "DELETE Response" $deleteResponse

# 9️ VERIFY deletion by attempting GET
try {
    $getDeleted = Invoke-RestMethod -Uri "http://localhost:8500/transactions/$shortId" -Headers $headers
    Show-Result "GET After DELETE (Should Fail)" $getDeleted
} catch {
    Write-Host "===== GET After DELETE ====="
    Write-Host "Transaction with ID $shortId not found (404) "
    Write-Host "`n"
}

# 10️ LIST all transactions (after deletion)
$allAfter = Invoke-RestMethod -Uri "http://localhost:8500/transactions" -Headers $headers
Show-Result "All Transactions After DELETE" $allAfter
