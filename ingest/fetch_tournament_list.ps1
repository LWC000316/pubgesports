# 공식 API 가 아는 대회 전체 목록을 받는다. 호출 1회.
#
#   powershell -NoProfile -File ingest/fetch_tournament_list.ps1
#
# 결과: intermediate_results/all_tournaments.json
# 키는 사용자 환경변수에서 읽으며 화면에 출력하지 않는다.

$ErrorActionPreference = 'Stop'

$key = [Environment]::GetEnvironmentVariable('PUBG_API_KEY', 'User')
if (-not $key) { Write-Output 'PUBG_API_KEY 가 없습니다.'; exit 1 }
$headers = @{ Authorization = "Bearer $key"; Accept = 'application/vnd.api+json' }

$root = Split-Path $PSScriptRoot -Parent
$dest = Join-Path $root 'intermediate_results/all_tournaments.json'

$r = Invoke-RestMethod -Uri 'https://api.pubg.com/tournaments' -Headers $headers -TimeoutSec 60
$r | ConvertTo-Json -Depth 10 | Set-Content -Path $dest -Encoding UTF8

Write-Output "대회 $($r.data.Count)개 -> $dest"
