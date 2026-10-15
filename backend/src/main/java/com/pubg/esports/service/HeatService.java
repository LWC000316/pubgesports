package com.pubg.esports.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pubg.esports.dto.HeatMapSummaryDto;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * 히트엔딩 — 여러 경기를 맵마다 모아 센 값
 * (`primary_data/heat/&lt;맵&gt;.json`, `ingest/build_heat.py` 가 만든다).
 *
 * 매치로그와 같은 이유로 파일에서 바로 읽는다. 맵당 40~60KB 라 한 장씩
 * 흘려보내면 되고, 목록만 기동 뒤 첫 요청에 한 번 만들어 들고 있는다.
 */
@Slf4j
@Service
public class HeatService {

    private static final String DIR = "primary_data/heat";

    private final ObjectMapper mapper = new ObjectMapper();
    private volatile List<HeatMapSummaryDto> summaries;

    /** 어떤 맵이 있는지. 경기가 많은 맵부터. */
    public List<HeatMapSummaryDto> listMaps() {
        List<HeatMapSummaryDto> cached = summaries;
        if (cached != null) {
            return cached;
        }
        File dir = resolve(DIR);
        if (dir == null) {
            return Collections.emptyList();
        }
        File[] files = dir.listFiles((d, n) -> n.endsWith(".json"));
        if (files == null) {
            return Collections.emptyList();
        }
        List<HeatMapSummaryDto> out = new ArrayList<>();
        for (File f : files) {
            try {
                JsonNode root = mapper.readTree(f);
                out.add(HeatMapSummaryDto.builder()
                        .map(root.path("map").asText())
                        .mapLabel(root.path("mapLabel").asText())
                        .matches(root.path("matches").asInt())
                        .stages(root.path("stages").asInt())
                        .build());
            } catch (Exception e) {
                log.warn("히트 요약 읽기 실패 [{}]: {}", f.getName(), e.getMessage());
            }
        }
        out.sort(Comparator.comparingInt(HeatMapSummaryDto::getMatches).reversed());
        summaries = out;
        return out;
    }

    /** 맵 하나의 집계 전체. 그대로 흘려보낸다. */
    public String read(String map) {
        File dir = resolve(DIR);
        if (dir == null) {
            return null;
        }
        File file = new File(dir, safe(map) + ".json");
        if (!file.isFile()) {
            return null;
        }
        try {
            return new String(Files.readAllBytes(file.toPath()), StandardCharsets.UTF_8);
        } catch (Exception e) {
            log.error("히트 집계 읽기 실패 [{}]: {}", map, e.getMessage());
            return null;
        }
    }

    /** 경로 조작을 막는다. 맵 이름은 영숫자와 밑줄뿐이다. */
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
