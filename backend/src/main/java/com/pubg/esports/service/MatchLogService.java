package com.pubg.esports.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pubg.esports.dto.MatchSummaryDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/**
 * primary_data/matchlogs/&lt;대회id&gt;/&lt;경기id&gt;.json 을 읽어 준다.
 *
 * 다른 아카이브와 달리 기동 시 메모리에 올리지 않는다. 경기당 수백 KB 이고
 * 한 번에 한 경기만 보기 때문이다. 다만 **목록**은 한 단계의 모든 파일을 열어야
 * 만들 수 있어 단계별로 한 번만 만들고 캐시한다.
 */
@Slf4j
@Service
public class MatchLogService {

    private static final String DIR = "primary_data/matchlogs";
    /** 경기 순서를 적어 둔 파일. 경기가 아니므로 목록에서 빼야 한다. */
    private static final String ORDER_FILE = "_order.json";

    private final ObjectMapper mapper = new ObjectMapper();
    private final Map<String, List<MatchSummaryDto>> cache = new ConcurrentHashMap<>();

    /** 그 대회에서 매치로그를 가진 경기들. 순서를 아는 단계는 경기 순서대로. */
    public List<MatchSummaryDto> listMatches(String tournamentId) {
        return cache.computeIfAbsent(safe(tournamentId), this::buildList);
    }

    private List<MatchSummaryDto> buildList(String tournamentId) {
        File dir = resolve(DIR + "/" + tournamentId);
        if (dir == null) {
            return Collections.emptyList();
        }
        File[] files = dir.listFiles(
                (d, n) -> n.endsWith(".json") && !n.startsWith("_"));
        if (files == null) {
            return Collections.emptyList();
        }

        Map<String, String> startedAt = readOrder(dir);
        List<MatchSummaryDto> rows = new ArrayList<>();
        for (File f : files) {
            MatchSummaryDto row = summarize(f, startedAt);
            if (row != null) {
                rows.add(row);
            }
        }
        // 시작 시각을 아는 것이 먼저, 시각 순으로. 모르는 것은 뒤에 파일 이름 순으로
        // 붙인다 — 섞어 세면 "몇 경기" 가 거짓이 된다.
        rows.sort(Comparator
                .comparing((MatchSummaryDto r) -> r.getStartedAt() == null)
                .thenComparing(r -> r.getStartedAt() == null ? r.getId() : r.getStartedAt()));
        return rows;
    }

    /** 경기id -> 시작 시각. ingest/build_match_order.py 가 만든다. */
    private Map<String, String> readOrder(File dir) {
        File f = new File(dir, ORDER_FILE);
        if (!f.isFile()) {
            return Collections.emptyMap();
        }
        try {
            JsonNode root = mapper.readTree(f);
            Map<String, String> out = new LinkedHashMap<>();
            for (JsonNode m : root.path("matches")) {
                String id = m.path("id").asText(null);
                String at = m.path("startedAt").asText(null);
                if (id != null && at != null) {
                    out.put(id, at);
                }
            }
            return out;
        } catch (Exception e) {
            log.warn("경기 순서 읽기 실패 [{}]: {}", dir.getName(), e.getMessage());
            return Collections.emptyMap();
        }
    }

    private MatchSummaryDto summarize(File f, Map<String, String> startedAt) {
        try {
            JsonNode root = mapper.readTree(f);
            String id = f.getName().replace(".json", "");
            // 로그 자체에 시작 시각이 적혀 있으면(최근에 뽑은 것) 그것을 먼저 쓴다.
            String at = root.path("startedAt").isTextual()
                    ? root.get("startedAt").asText() : startedAt.get(id);
            return MatchSummaryDto.builder()
                    .id(id)
                    .startedAt(at)
                    .map(root.path("mapLabel").asText(root.path("map").asText(null)))
                    .duration(root.path("duration").asInt())
                    .kills(root.path("kills").size())
                    .winner(winnerOf(root))
                    .build();
        } catch (Exception e) {
            log.warn("매치로그 요약 실패 [{}]: {}", f.getName(), e.getMessage());
            return null;
        }
    }

    /**
     * 치킨을 먹은 팀. 킬 기록의 피해자 명단에 한 명도 들어 있지 않은 팀을 찾는다.
     * PGS 9 결승 15경기를 집계 파일의 WWCD 수와 맞춰 봤고 전부 일치했다.
     * 팀이 둘 이상 남으면(기록이 모자란 옛 경기) 지어내지 않고 비운다.
     */
    private String winnerOf(JsonNode root) {
        Map<String, String> teamOf = new HashMap<>();
        for (JsonNode t : root.path("tracks")) {
            String name = t.path("name").asText(null);
            if (name == null) {
                continue;
            }
            String team = t.path("team").asText(null);
            teamOf.put(name, team == null || team.isBlank()
                    ? t.path("nickname").asText(name) : team);
        }
        Set<String> dead = new HashSet<>();
        for (JsonNode k : root.path("kills")) {
            String v = k.path("victim").asText(null);
            if (v != null) {
                dead.add(v);
            }
        }
        Set<String> alive = new HashSet<>();
        for (Map.Entry<String, String> e : teamOf.entrySet()) {
            if (!dead.contains(e.getKey())) {
                alive.add(e.getValue());
            }
        }
        return alive.size() == 1 ? alive.iterator().next() : null;
    }

    public String read(String tournamentId, String matchId) {
        File dir = resolve(DIR + "/" + safe(tournamentId));
        if (dir == null) {
            return null;
        }
        File file = new File(dir, safe(matchId) + ".json");
        if (!file.isFile()) {
            return null;
        }
        try {
            return new String(Files.readAllBytes(file.toPath()), StandardCharsets.UTF_8);
        } catch (Exception e) {
            log.error("매치로그 읽기 실패 [{}/{}]: {}", tournamentId, matchId, e.getMessage());
            return null;
        }
    }

    /** 경로 조작을 막는다. 대회·경기 id 는 영숫자와 하이픈뿐이다. */
    private String safe(String value) {
        return value == null ? "" : value.replaceAll("[^A-Za-z0-9_-]", "");
    }

    private File resolve(String relativePath) {
        File file = new File(relativePath);
        if (file.isDirectory()) {
            return file;
        }
        file = new File("../" + relativePath);
        return file.isDirectory() ? file : null;
    }
}
