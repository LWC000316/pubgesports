# ingest/stage_ids.txt 에 적힌 대회 단계를 차례로 내려받는다.
#
#   powershell -NoProfile -File ingest/fetch_all.ps1
#
# 이어받기를 지원한다. 이미 받은 경기는 건너뛰므로 중간에 끊겨도 다시 돌리면 된다.
# API 는 10회/분 제한이라 334단계(약 3,500경기)에 6~7시간이 걸린다.
# 진행 상황은 ingest/fetch_all.progress 에 한 줄씩 남는다.

param(
    [int]$DelaySeconds = 6,
    # 이 분을 넘기면 받던 것을 마치고 깔끔히 끝낸다. GitHub Actions 는 작업 하나가
    # 6시간을 넘으면 강제로 죽이는데, 그러면 뒤따르는 집계·커밋이 통째로 날아간다.
    [int]$MaxMinutes = 0,
    # 이미 집계된(primary_data/tournaments 에 결과가 있는) 단계는 건너뛴다.
    # 커밋된 집계 결과가 곧 진행 표시라서, 서버는 원본을 보관하지 않아도 된다.
    [switch]$SkipBuilt
)

$ErrorActionPreference = 'Continue'
$root = Split-Path $PSScriptRoot -Parent
$list = Join-Path $PSScriptRoot 'stage_ids.txt'
$prog = Join-Path $PSScriptRoot 'fetch_all.progress'

# 윈도우에서는 사용자 환경변수, CI 에서는 보통 프로세스 환경변수에 들어온다.
$key = $env:PUBG_API_KEY
if (-not $key -and $IsWindows -ne $false) {
    $key = [Environment]::GetEnvironmentVariable('PUBG_API_KEY', 'User')
}
if (-not $key) { Write-Output 'PUBG_API_KEY 가 없습니다.'; exit 1 }
$headers = @{ Authorization = "Bearer $key"; Accept = 'application/vnd.api+json' }

$lines = Get-Content $list
$built = Join-Path $root 'primary_data/tournaments'
$deadline = if ($MaxMinutes -gt 0) { (Get-Date).AddMinutes($MaxMinutes) } else { $null }
$n = 0
foreach ($line in $lines) {
    $n++
    $parts = $line -split "`t"
    if ($parts.Count -lt 3) { continue }
    $date = $parts[0]; $series = $parts[1]; $tid = $parts[2]

    if ($deadline -and (Get-Date) -gt $deadline) {
        "시간이 다 돼 여기서 멈춥니다 ($n/$($lines.Count)). 다시 돌리면 이어받습니다." |
            Tee-Object -FilePath $prog -Append
        break
    }
    # 집계 결과가 있어도 **덜 받은 단계는 다시 받는다.** 집계 결과에 공식 API 가
    # 알려준 경기 수(matchesListed)와 실제 경기 수(matchCount)가 함께 들어 있어서,
    # 그게 다르면 네트워크 오류로 몇 경기를 놓친 것이다. 그냥 건너뛰면 영영 메운다.
    if ($SkipBuilt) {
        $builtFile = Join-Path $built "$tid.json"
        if (Test-Path $builtFile) {
            $complete = $true
            try {
                $b = Get-Content $builtFile -Raw | ConvertFrom-Json
                $voided = if ($null -ne $b.matchesVoided) { $b.matchesVoided } else { 0 }
                if ($null -ne $b.matchesListed -and
                        ($b.matchesListed - $voided) -gt $b.matchCount) {
                    $complete = $false
                }
            } catch { $complete = $true }
            if ($complete) { continue }
            "[$n/$($lines.Count)] $tid 는 덜 받아서 다시 받습니다." |
                Tee-Object -FilePath $prog -Append
        }
    }

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
