package com.pubg.esports.service;

import com.pubg.esports.domain.HotSeed;
import com.pubg.esports.domain.Player;
import com.pubg.esports.domain.PlayerView;
import com.pubg.esports.dto.HotPlayerDto;
import com.pubg.esports.repository.HotSeedRepository;
import com.pubg.esports.repository.PlayerRepository;
import com.pubg.esports.repository.PlayerViewRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.temporal.WeekFields;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;

/**
 * HOT 탭. 선수 조회수를 기간별로 세고 상위 N명을 돌려준다.
 *
 * 선수 정보는 여기서 만들지 않는다 — 자연키로 players 를 찾아 그 데이터를 그대로 쓴다.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class HotPlayerService {

    private final PlayerRepository playerRepository;
    private final PlayerViewRepository playerViewRepository;
    private final HotSeedRepository hotSeedRepository;

    /** ISO 주차. 이 값이 바뀌면 조회수가 자연히 새로 쌓인다 — 초기화 작업이 필요 없다. */
    public static String currentPeriod() {
        LocalDate today = LocalDate.now();
        WeekFields wf = WeekFields.ISO;
        return String.format("%d-W%02d",
                today.get(wf.weekBasedYear()), today.get(wf.weekOfWeekBasedYear()));
    }

    /**
     * 선수 한 명의 조회를 기록한다. 선수가 어느 팀 소속인지는 DB 에서 읽어
     * 자연키를 만든다 — 호출자가 보낸 값을 믿지 않는다.
     */
    @Transactional
    public void recordView(Long playerId) {
        Player player = playerRepository.findById(playerId).orElse(null);
        if (player == null || player.getTeam() == null) {
            log.warn("조회 기록 실패: 선수 {} 를 찾을 수 없거나 소속 팀이 없습니다.", playerId);
            return;
        }
        String league = player.getTeam().getLeague();
        String team = player.getTeam().getName();
        String nickname = player.getNickname();
        String period = currentPeriod();

        PlayerView view = playerViewRepository
                .findByLeagueAndTeamNameAndNicknameAndPeriod(league, team, nickname, period)
                .orElseGet(() -> playerViewRepository.save(PlayerView.builder()
                        .league(league).teamName(team).nickname(nickname).period(period).build()));
        view.increase();
    }

    /**
     * 상위 N명. 이번 기간 조회수가 많은 순, 조회수가 같으면 초기 순위(hot_seeds) 순.
     * 조회가 아직 없으면 초기 12명만 나온다.
     */
    @Transactional(readOnly = true)
    public List<HotPlayerDto> getHotPlayers(int limit) {
        String period = currentPeriod();

        // 자연키 -> 이번 기간 조회수
        Map<String, Long> counts = new LinkedHashMap<>();
        for (PlayerView v : playerViewRepository.findAll()) {
            if (period.equals(v.getPeriod())) {
                counts.put(key(v.getLeague(), v.getTeamName(), v.getNickname()), v.getViewCount());
            }
        }

        // 자연키 -> 초기 순위
        Map<String, HotSeed> seeds = new LinkedHashMap<>();
        for (HotSeed s : hotSeedRepository.findAllByOrderBySeedRankAsc()) {
            seeds.put(key(s.getLeague(), s.getTeamName(), s.getNickname()), s);
        }

        List<String> candidates = new ArrayList<>(counts.keySet());
        for (String k : seeds.keySet()) {
            if (!candidates.contains(k)) {
                candidates.add(k);
            }
        }

        List<HotPlayerDto> out = new ArrayList<>();
        for (String k : candidates) {
            String[] parts = k.split("\u001f", -1);
            Optional<Player> found = playerRepository.findByNaturalKey(parts[0], parts[1], parts[2]);
            if (found.isEmpty()) {
                // 로스터가 바뀌어 더는 없는 선수. 조회수는 남겨두고 화면에서만 뺀다.
                continue;
            }
            HotSeed seed = seeds.get(k);
            out.add(HotPlayerDto.from(found.get(), counts.getOrDefault(k, 0L),
                    seed != null ? seed.getSeedRank() : null,
                    seed != null ? seed.getSource() : null));
        }

        out.sort(Comparator
                .comparingLong(HotPlayerDto::getViewCount).reversed()
                .thenComparing(d -> d.getSeedRank() == null ? Integer.MAX_VALUE : d.getSeedRank())
                .thenComparing(HotPlayerDto::getNickname));

        return out.size() > limit ? out.subList(0, limit) : out;
    }

    private static String key(String league, String team, String nickname) {
        return league + "\u001f" + team + "\u001f" + nickname;
    }
}
