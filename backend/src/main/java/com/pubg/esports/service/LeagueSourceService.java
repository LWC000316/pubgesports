package com.pubg.esports.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pubg.esports.dto.LeagueSourceDto;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * primary_data/_sources.json 을 기동 시 한 번 읽어 들고 있는다.
 * 시드 파일과 같은 자리에 있는 정적 파일이라 DB 에 넣지 않는다.
 */
@Slf4j
@Service
public class LeagueSourceService {

    private static final String SOURCES_PATH = "primary_data/_sources.json";

    private final ObjectMapper objectMapper = new ObjectMapper();
    private Map<String, LeagueSourceDto> sources = Collections.emptyMap();

    @PostConstruct
    void load() {
        File file = resolve(SOURCES_PATH);
        if (file == null) {
            log.warn("{} 파일이 없어 수집 출처 정보를 제공하지 않습니다.", SOURCES_PATH);
            return;
        }
        try {
            JsonNode leagues = objectMapper.readTree(file).path("leagues");
            Map<String, LeagueSourceDto> loaded = new LinkedHashMap<>();
            leagues.fieldNames().forEachRemaining(league ->
                    loaded.put(league.toUpperCase(),
                            LeagueSourceDto.from(league, leagues.path(league))));
            sources = loaded;
            log.info("수집 출처 정보 {}개 리그 적재", sources.size());
        } catch (Exception e) {
            log.error("수집 출처 정보 로딩 실패: {}", e.getMessage(), e);
        }
    }

    public List<LeagueSourceDto> getAll() {
        return new ArrayList<>(sources.values());
    }

    public LeagueSourceDto get(String league) {
        return league == null ? null : sources.get(league.toUpperCase());
    }

    private File resolve(String relativePath) {
        File file = new File(relativePath);
        if (file.exists()) {
            return file;
        }
        file = new File("../" + relativePath);
        return file.exists() ? file : null;
    }
}
