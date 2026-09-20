package com.pubg.esports.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Service
@RequiredArgsConstructor
public class PubgOfficialApiService {

    @Value("${pubg.api.base-url:https://api.pubg.com}")
    private String baseUrl;

    @Value("${pubg.api.key}")
    private String apiKey;

    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    // 10 RPM Rate Limit 보호를 위한 지능형 인메모리 캐시 (1일 캐싱)
    private final Map<String, List<Map<String, Object>>> tournamentCache = new ConcurrentHashMap<>();
    private final Map<String, Object> matchCache = new ConcurrentHashMap<>();

    // 허용된 권역 대회 및 세계 대회 필터 목록 (PWS, PCL, PGS, PGC, PNC, EWC)
    private static final List<String> ALLOWED_KEYWORDS = List.of(
            "pws", "pcl", "pgs", "pgc", "pnc", "ewc"
    );

    /**
     * 크래프톤 공식 PUBG Developer API에서 실시간 토너먼트 목록을 가져오고
     * PWS, PCL (권역 대회) 및 PGS, PGC, PNC, EWC (세계 대회)만 선별 필터링
     */
    public List<Map<String, Object>> getFilteredOfficialTournaments() {
        // 1. 캐시 확인 (10 RPM 보존)
        if (tournamentCache.containsKey("MAJOR_TOURNAMENTS")) {
            return tournamentCache.get("MAJOR_TOURNAMENTS");
        }

        List<Map<String, Object>> result = new ArrayList<>();

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + apiKey);
            headers.set("Accept", "application/vnd.api+json");
            headers.set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
            HttpEntity<String> entity = new HttpEntity<>(headers);

            String url = baseUrl + "/tournaments";
            log.info("크래프톤 공식 PUBG API 호출 중: {}", url);
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                JsonNode root = objectMapper.readTree(response.getBody());
                JsonNode dataNode = root.get("data");

                if (dataNode != null && dataNode.isArray()) {
                    for (JsonNode item : dataNode) {
                        String tournamentId = item.get("id").asText();
                        String lowerId = tournamentId.toLowerCase();

                        for (String kw : ALLOWED_KEYWORDS) {
                            if (lowerId.contains(kw)) {
                                Map<String, Object> tMap = new HashMap<>();
                                tMap.put("id", tournamentId);
                                tMap.put("name", formatTournamentName(tournamentId, kw.toUpperCase()));
                                tMap.put("category", categorizeTournament(kw.toUpperCase()));
                                tMap.put("keyword", kw.toUpperCase());
                                tMap.put("source", "KRAFTON_OFFICIAL_API");
                                result.add(tMap);
                                break;
                            }
                        }
                    }
                }
            }
            log.info("공식 API에서 필터링된 주요 대회 총 {}건 로드 완료", result.size());
        } catch (Exception e) {
            log.warn("공식 PUBG API 호출 실패: {}", e.getMessage());
        }

        if (result.isEmpty()) {
            // 호출이 실패하면 빈 목록을 그대로 반환한다.
            // 예전에는 하드코딩한 대회 목록을 공식 API 응답인 것처럼 돌려줬는데,
            // 검증되지 않은 값이 검증된 것처럼 보이므로 폴백을 없앴다.
            log.warn("공식 API에서 가져온 대회가 없습니다. 빈 목록을 반환합니다.");
            return result;
        }

        // 캐시 저장 (실패 응답은 캐시하지 않는다)
        tournamentCache.put("MAJOR_TOURNAMENTS", result);
        return result;
    }

    /**
     * 특정 공식 토너먼트의 세부 매치 목록 조회
     */
    public List<String> getTournamentMatches(String tournamentId) {
        List<String> matchIds = new ArrayList<>();
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.set("Authorization", "Bearer " + apiKey);
            headers.set("Accept", "application/vnd.api+json");
            HttpEntity<String> entity = new HttpEntity<>(headers);

            String url = baseUrl + "/tournaments/" + tournamentId;
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                JsonNode root = objectMapper.readTree(response.getBody());
                JsonNode matchesNode = root.path("data").path("relationships").path("matches").path("data");
                if (matchesNode.isArray()) {
                    for (JsonNode m : matchesNode) {
                        matchIds.add(m.get("id").asText());
                    }
                }
            }
        } catch (Exception e) {
            log.warn("토너먼트 {} 매치 조회 실패: {}", tournamentId, e.getMessage());
        }
        return matchIds;
    }

    public String categorizeTournament(String keyword) {
        if (keyword.equals("PGS") || keyword.equals("PGC") || keyword.equals("PNC") || keyword.equals("EWC")) {
            return "GLOBAL (세계 대회)";
        }
        if (keyword.equals("PWS")) {
            return "REGIONAL: KR (대한민국 PWS)";
        }
        if (keyword.equals("PCL")) {
            return "REGIONAL: CN (중국 PCL)";
        }
        return "REGIONAL (권역 대회)";
    }

    private String formatTournamentName(String id, String kw) {
        return "[" + kw + "] " + id.replace("-", " ").toUpperCase();
    }

}
