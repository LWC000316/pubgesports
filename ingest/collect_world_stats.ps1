# 2026년 세계대회(PGS·PNC·EWC)의 선수별 킬·데미지를 모은다.
#
# HOT 탭의 초기 12명을 정하는 근거다. 조회수가 쌓이기 전에 화면을 채울 순위이며
# 조회수가 쌓이면 자연히 밀려난다.
#
# 공식 PUBG API 를 쓴다 - 킬·데미지는 리퀴피디아에 없고 이쪽이 원본이다.
# 키는 사용자 환경변수에서 읽으며 화면에 출력하지 않는다.
#
#   powershell -NoProfile -File ingest/collect_world_stats.ps1
#
# 결과: intermediate_results/world_stats_2026.json

$ErrorActionPreference = 'Stop'

$key = [Environment]::GetEnvironmentVariable('PUBG_API_KEY', 'User')
if (-not $key) { Write-Output 'PUBG_API_KEY 가 없습니다.'; exit 1 }
$headers = @{ Authorization = "Bearer $key"; Accept = 'application/vnd.api+json' }

# 2026년 세계대회. 예선·그룹스테이지까지 넣으면 경기 수가 너무 늘어나
# 각 대회의 본선(그랜드 파이널·메인 토너먼트)만 본다.
$tournaments = @(
    @{ id = 'as-pgs9gf';  name = 'PGS 9 Grand Finals' },
    @{ id = 'as-pgs8fsg'; name = 'PGS 8 Final Stage' },
    @{ id = 'as-pgs7fsg'; name = 'PGS 7 Final Stage' },
    @{ id = 'as-pnc26gf'; name = 'PNC 2026 Grand Finals' },
    @{ id = 'eu-26ewcmt'; name = 'EWC 2026 Main Tournament' }
)

# 닉네임 -> 누적치
$agg = @{}
$matchTotal = 0

foreach ($t in $tournaments) {
    Write-Output "[$($t.name)] 경기 목록 조회"
    try {
        $r = Invoke-RestMethod -Uri "https://api.pubg.com/tournaments/$($t.id)" -Headers $headers -TimeoutSec 60
    } catch {
        Write-Output "  대회 조회 실패: $($_.Exception.Message)"
        continue
    }
    $matches = @($r.included | Where-Object { $_.type -eq 'match' })
    Write-Output "  경기 $($matches.Count)개"
    Start-Sleep -Seconds 6

    foreach ($m in $matches) {
        try {
            $md = Invoke-RestMethod -Uri "https://api.pubg.com/shards/tournament/matches/$($m.id)" -Headers $headers -TimeoutSec 60
        } catch {
            Write-Output "  경기 $($m.id) 실패: $($_.Exception.Message)"
            Start-Sleep -Seconds 8
            continue
        }
        $matchTotal++
        foreach ($p in ($md.included | Where-Object { $_.type -eq 'participant' })) {
            $s = $p.attributes.stats
            $n = $s.name
            if (-not $n) { continue }
            if (-not $agg.ContainsKey($n)) {
                $agg[$n] = @{ name = $n; kills = 0; damage = 0.0; matches = 0; events = @() }
            }
            $agg[$n].kills   += [int]$s.kills
            $agg[$n].damage  += [double]$s.damageDealt
            $agg[$n].matches += 1
            if ($agg[$n].events -notcontains $t.name) { $agg[$n].events += $t.name }
        }
        Start-Sleep -Seconds 6
    }
}

$rows = $agg.Values | ForEach-Object {
    [PSCustomObject]@{
        name    = $_.name
        kills   = $_.kills
        damage  = [math]::Round($_.damage, 1)
        matches = $_.matches
        events  = ($_.events -join ' / ')
    }
} | Sort-Object -Property kills, damage -Descending

$out = Join-Path (Split-Path $PSScriptRoot -Parent) 'intermediate_results/world_stats_2026.json'
$rows | ConvertTo-Json -Depth 4 | Set-Content -Path $out -Encoding UTF8

Write-Output ""
Write-Output "경기 $matchTotal 개, 선수 $($rows.Count) 명 -> $out"
Write-Output "상위 20명:"
$rows | Select-Object -First 20 | ForEach-Object {
    Write-Output ("  {0,-18} 킬 {1,3}  데미지 {2,9}  {3}경기" -f $_.name, $_.kills, $_.damage, $_.matches)
}
