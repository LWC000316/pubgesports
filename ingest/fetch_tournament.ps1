# 대회 하나의 경기 원본을 그대로 내려받는다. 집계는 하지 않는다.
#
# 네트워크(키가 필요한 부분)와 집계(로직)를 분리한다. 이 스크립트는 받아서 저장만
# 하고, build_tournament_seed.py 가 그 파일들을 읽어 순위표를 만든다. 그래야 집계
# 로직을 고칠 때마다 API 를 다시 때리지 않는다 (10회/분 제한).
#
#   powershell -NoProfile -File ingest/fetch_tournament.ps1 as-pgs9gf
#
# 결과: intermediate_results/tournaments/<대회id>/  (tournament.json + 경기별 json)
#
# 키는 사용자 환경변수에서 읽으며 화면에 출력하지 않는다.

param(
    [Parameter(Mandatory = $true)][string]$TournamentId,
    [int]$DelaySeconds = 6
)

$ErrorActionPreference = 'Stop'

# 윈도우에서는 사용자 환경변수, CI 에서는 프로세스 환경변수로 들어온다.
$key = $env:PUBG_API_KEY
if (-not $key -and $IsWindows -ne $false) {
    $key = [Environment]::GetEnvironmentVariable('PUBG_API_KEY', 'User')
}
if (-not $key) { Write-Output 'PUBG_API_KEY 가 없습니다.'; exit 1 }
$headers = @{ Authorization = "Bearer $key"; Accept = 'application/vnd.api+json' }

$root = Split-Path $PSScriptRoot -Parent
$dir = Join-Path $root "intermediate_results/tournaments/$TournamentId"
New-Item -ItemType Directory -Force -Path $dir | Out-Null

Write-Output "[$TournamentId] 경기 목록 조회"
$t = Invoke-RestMethod -Uri "https://api.pubg.com/tournaments/$TournamentId" -Headers $headers -TimeoutSec 60
$t | ConvertTo-Json -Depth 10 | Set-Content -Path (Join-Path $dir 'tournament.json') -Encoding UTF8

$matches = @($t.included | Where-Object { $_.type -eq 'match' })
Write-Output "  경기 $($matches.Count)개"

$done = 0
$skipped = 0
foreach ($m in $matches) {
    $dest = Join-Path $dir "match_$($m.id).json"
    if (Test-Path $dest) { $skipped++; continue }   # 이어받기
    Start-Sleep -Seconds $DelaySeconds
    try {
        $d = Invoke-RestMethod -Uri "https://api.pubg.com/shards/tournament/matches/$($m.id)" -Headers $headers -TimeoutSec 60
        $d | ConvertTo-Json -Depth 10 | Set-Content -Path $dest -Encoding UTF8
        $done++
        Write-Output "  [$done/$($matches.Count)] $($m.id)"
    } catch {
        Write-Output "  실패 $($m.id): $($_.Exception.Message)"
    }
}

Write-Output ""
Write-Output "새로 받음 $done 개, 이미 있어 건너뜀 $skipped 개 -> $dir"
Write-Output "다음: python ingest/build_tournament_seed.py $TournamentId"
