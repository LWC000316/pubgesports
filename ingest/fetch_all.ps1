# ingest/stage_ids.txt 에 적힌 대회 단계를 차례로 내려받는다.
#
#   powershell -NoProfile -File ingest/fetch_all.ps1
#
# 이어받기를 지원한다. 이미 받은 경기는 건너뛰므로 중간에 끊겨도 다시 돌리면 된다.
# API 는 10회/분 제한이라 334단계(약 3,500경기)에 6~7시간이 걸린다.
# 진행 상황은 ingest/fetch_all.progress 에 한 줄씩 남는다.

param([int]$DelaySeconds = 6)

$ErrorActionPreference = 'Continue'
$root = Split-Path $PSScriptRoot -Parent
$list = Join-Path $PSScriptRoot 'stage_ids.txt'
$prog = Join-Path $PSScriptRoot 'fetch_all.progress'

$key = [Environment]::GetEnvironmentVariable('PUBG_API_KEY', 'User')
if (-not $key) { Write-Output 'PUBG_API_KEY 가 없습니다.'; exit 1 }
$headers = @{ Authorization = "Bearer $key"; Accept = 'application/vnd.api+json' }

$lines = Get-Content $list
$n = 0
foreach ($line in $lines) {
    $n++
    $parts = $line -split "`t"
    if ($parts.Count -lt 3) { continue }
    $date = $parts[0]; $series = $parts[1]; $tid = $parts[2]

    $dir = Join-Path $root "intermediate_results/tournaments/$tid"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $tfile = Join-Path $dir 'tournament.json'

    try {
        if (Test-Path $tfile) {
            $t = Get-Content $tfile -Raw | ConvertFrom-Json
        } else {
            Start-Sleep -Seconds $DelaySeconds
            $t = Invoke-RestMethod -Uri "https://api.pubg.com/tournaments/$tid" -Headers $headers -TimeoutSec 60
            $t | ConvertTo-Json -Depth 10 | Set-Content -Path $tfile -Encoding UTF8
        }
    } catch {
        "[$n/$($lines.Count)] $tid 목록 실패: $($_.Exception.Message)" | Tee-Object -FilePath $prog -Append
        continue
    }

    $matches = @($t.included | Where-Object { $_.type -eq 'match' })
    $got = 0; $skip = 0; $fail = 0
    foreach ($m in $matches) {
        $dest = Join-Path $dir "match_$($m.id).json"
        if (Test-Path $dest) { $skip++; continue }
        Start-Sleep -Seconds $DelaySeconds
        try {
            $d = Invoke-RestMethod -Uri "https://api.pubg.com/shards/tournament/matches/$($m.id)" -Headers $headers -TimeoutSec 60
            $d | ConvertTo-Json -Depth 10 | Set-Content -Path $dest -Encoding UTF8
            $got++
        } catch { $fail++ }
    }
    "[$n/$($lines.Count)] $date $series $tid - 경기 $($matches.Count) (새로 $got, 기존 $skip, 실패 $fail)" |
        Tee-Object -FilePath $prog -Append
}
Write-Output "끝났습니다."
