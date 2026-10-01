package com.pubg.esports.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * primary_data/matchlogs/&lt;대회id&gt;/&lt;경기id&gt;.json 을 읽어 준다.
 *
 * 다른 아카이브와 달리 기동 시 메모리에 올리지 않는다. 경기당 수백 KB 이고
 * 한 번에 한 경기만 보기 때문이다.
 */
@Slf4j
@Service
public class MatchLogService {

    private static final String DIR = "primary_data/matchlogs";

    public List<String> listMatchIds(String tournamentId) {
        File dir = resolve(DIR + "/" + safe(tournamentId));
        if (dir == null) {
            return Collections.emptyList();
        }
        File[] files = dir.listFiles((d, n) -> n.endsWith(".json"));
        if (files == null) {
            return Collections.emptyList();
        }
        List<String> ids = new ArrayList<>();
        for (File f : files) {
            ids.add(f.getName().replace(".json", ""));
        }
        Collections.sort(ids);
        return ids;
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
