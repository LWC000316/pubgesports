package com.pubg.esports.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.pubg.esports.dto.TournamentArchiveDto;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * primary_data/tournaments/*.json 을 기동 시 한 번 읽어 들고 있는다.
 *
 * 대회 기록은 런타임에 쌓이는 값이 아니라 정적 참조 자료다. 시드 파일과 같은 자리에
 * 두고 DB 에 넣지 않는다 (LeagueSourceService 와 같은 방식).
 *
 * 파일은 ingest/fetch_tournament.ps1 + ingest/build_tournament_seed.py 가 만든다.
 */
@Slf4j
@Service
public class TournamentArchiveService {

    private static final String DIR = "primary_data/tournaments";

    private final ObjectMapper objectMapper = new ObjectMapper();
    private volatile Map<String, TournamentArchiveDto> archives = Collections.emptyMap();

    /**
     * 적재했을 때의 디렉터리 상태 (파일 수 + 가장 최근 수정 시각).
     *
     * **수집기가 새 대회를 넣어도 화면에 안 나오던 이유가 여기였다.** 이
     * 서비스는 기동 때 한 번만 읽었다. 그래서 10월에 치른 PGS 가 저장소에
     * 들어온 뒤에도 돌고 있던 앱에는 영영 안 보였고, 사람이 서버를 껐다
     * 켜야 했다. 요청마다 디렉터리 상태를 견주어 바뀌었으면 다시 읽는다.
     * 파일 348개의 수정 시각을 보는 데 1밀리초가 안 걸린다.
     */
    private volatile String loadedStamp = "";

    @PostConstruct
    void load() {
        File dir = resolve(DIR);
        if (dir == null) {
            log.warn("{} 디렉터리가 없어 대회 아카이브를 제공하지 않습니다.", DIR);
            return;
        }
        File[] files = dir.listFiles((d, name) -> name.endsWith(".json"));
        if (files == null || files.length == 0) {
            log.warn("{} 에 대회 파일이 없습니다.", DIR);
            return;
        }

        Map<String, TournamentArchiveDto> loaded = new LinkedHashMap<>();
        for (File f : files) {
            try {
                TournamentArchiveDto dto = TournamentArchiveDto.from(objectMapper.readTree(f));
                if (dto.getId() == null || dto.getId().isEmpty()) {
                    log.warn("{}: id 가 없어 건너뜁니다.", f.getName());
                    continue;
                }
                loaded.put(dto.getId(), dto);
            } catch (Exception e) {
                log.error("대회 파일 로딩 실패 [{}]: {}", f.getName(), e.getMessage(), e);
            }
        }
        archives = loaded;
        loadedStamp = stamp(dir);
        log.info("=== 대회 아카이브 {}건 적재 ===", archives.size());
    }

    /** 디렉터리가 바뀌었으면 다시 읽는다. 안 바뀌었으면 아무것도 하지 않는다. */
    private void reloadIfChanged() {
        File dir = resolve(DIR);
        if (dir == null) {
            return;
        }
        String now = stamp(dir);
        if (now.equals(loadedStamp)) {
            return;
        }
        log.info("대회 파일이 바뀌어 다시 읽습니다 ({} -> {}).", loadedStamp, now);
        load();
    }

    /** 파일 수와 가장 최근 수정 시각. 내용까지 보지는 않는다. */
    private String stamp(File dir) {
        File[] files = dir.listFiles((d, name) -> name.endsWith(".json"));
        if (files == null) {
            return "";
        }
        long newest = 0L;
        for (File f : files) {
            newest = Math.max(newest, f.lastModified());
        }
        return files.length + ":" + newest;
    }

    /** category 가 null 이면 전부. 최신(createdAt 내림차순)으로 준다. */
    public List<TournamentArchiveDto> list(String category) {
        reloadIfChanged();
        List<TournamentArchiveDto> out = new ArrayList<>();
        for (TournamentArchiveDto dto : archives.values()) {
            if (category == null || category.equalsIgnoreCase(dto.getCategory())) {
                out.add(dto.toSummary());
            }
        }
        out.sort(Comparator.comparing(
                TournamentArchiveDto::getCreatedAt,
                Comparator.nullsLast(Comparator.reverseOrder())));
        return out;
    }

    public TournamentArchiveDto get(String id) {
        reloadIfChanged();
        return id == null ? null : archives.get(id);
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
