[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$response = Invoke-WebRequest -Uri "https://www.youtube.com/watch?v=aqz-KE-bpKQ" -UseBasicParsing
$html = $response.Content
if ($html -match 'ytInitialPlayerResponse\s*=\s*({.+?});') {
    $json = $matches[1]
    Set-Content -Path "yt_response.json" -Value $json
    Write-Host "yt_response.json saved."
} else {
    Write-Host "No ytInitialPlayerResponse found."
}
