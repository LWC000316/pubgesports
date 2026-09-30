package com.pubg.esports.config;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pubg.esports.domain.*;
import com.pubg.esports.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.io.File;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    /**
     * 검증된 리그 시드 파일. 리그를 추가할 때는 이 목록에 한 줄만 넣으면 된다.
     * 파일 스키마는 pws2_teams_verified.json 과 동일해야 한다.
     */
    private static final List<String> VERIFIED_SEEDS = List.of(
            "primary_data/pws2_teams_verified.json",
            "primary_data/pcl_teams_verified.json",
            "primary_data/emea_teams_verified.json",
            "primary_data/amer_teams_verified.json",
            "primary_data/pts_teams_verified.json",
            "primary_data/pvs_teams_verified.json"
    );

    private final TeamRepository teamRepository;
    private final PlayerRepository playerRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * auto   - 비어 있을 때만 적재 (기본)
     * always - 기동마다 팀·선수를 지우고 다시 적재. 시드 파일을 고친 뒤 한 번 쓴다
     * never  - 적재하지 않는다
     */
    @Value("${app.seed.mode:auto}")
    private String seedMode;

    @Override
    @Transactional
    public void run(String... args) {
        // 예전에는 ddl-auto: create 가 기동마다 스키마를 날려서 이 메서드가 항상
        // 빈 DB 에 적재했다. 이제 스키마와 데이터가 남으므로 적재 여부를 직접 정한다.
        if ("never".equalsIgnoreCase(seedMode)) {
            log.info("app.seed.mode=never 이므로 시드 적재를 건너뜁니다.");
            return;
        }

        long existing = teamRepository.count();
        if ("always".equalsIgnoreCase(seedMode)) {
            if (existing > 0) {
                log.info("app.seed.mode=always — 기존 팀 {}개와 소속 선수를 지우고 다시 적재합니다.",
                        existing);
                // deleteAllInBatch 는 JPA 연관을 타지 않는 단일 DELETE 라
                // player_settings·player_gears 의 FK 제약에 걸린다.
                // deleteAll 은 엔티티를 읽어 cascade = ALL 을 따라 자식까지 지운다.
                teamRepository.deleteAll();
                playerRepository.deleteAll();   // 팀이 없는 레거시 선수까지 정리
            }
        } else if (existing > 0) {
            log.info("이미 팀 {}개가 적재돼 있어 시드를 건너뜁니다. "
                    + "시드 파일을 고쳤다면 SEED_MODE=always 로 한 번 기동하세요.", existing);
            return;
        }

        Set<String> loadedTeamNames = new HashSet<>();

        // 검증된 시드를 먼저 전부 적재한다. 아래 레거시 파일은 로고가 플레이스홀더라
        // 덮어쓰면 안 되므로 순서가 중요하다.
        for (String seedPath : VERIFIED_SEEDS) {
            loadVerifiedTeams(seedPath, loadedTeamNames);
        }
        loadLegacyOfficialTeams(loadedTeamNames);
    }

    private void loadVerifiedTeams(String seedPath, Set<String> loadedTeamNames) {
        File jsonFile = resolveDataFile(seedPath);
        if (jsonFile == null) {
            log.warn("{} 파일이 없어 해당 리그 시드 적재를 건너뜁니다.", seedPath);
            return;
        }

        log.info("=== 검증 시드 적재 시작: {} ===", seedPath);
        try {
            JsonNode root = objectMapper.readTree(jsonFile);
            if (!root.isArray()) {
                log.warn("{} 의 최상위가 배열이 아닙니다.", seedPath);
                return;
            }

            int teamCount = 0;
            int playerCount = 0;

            for (JsonNode tNode : root) {
                String name = tNode.path("name").asText();
                if (name.isEmpty()) {
                    continue;
                }

                String region = tNode.path("region").asText("KR");

                // league 에 기본값을 주지 않는다. 누락된 팀이 조용히 다른 리그로
                // 섞여 들어가는 사고를 막기 위해 건너뛰고 경고만 남긴다.
                String league = tNode.path("league").asText("");
                if (league.isEmpty()) {
                    log.warn("{}: '{}' 팀에 league 값이 없어 건너뜁니다.", seedPath, name);
                    continue;
                }

                // 템플릿 문자열로 채우지 않는다. 시드에 없는 값은 비워 둔다.
                Team team = Team.builder()
                        .name(name)
                        .region(region)
                        .tag(tNode.path("tag").asText(null))
                        .seedType(tNode.path("seedType").asText(null))
                        .league(league)
                        .logoUrl(tNode.path("logoUrl").asText(""))
                        .build();

                teamRepository.save(team);
                loadedTeamNames.add(name.toLowerCase(Locale.ROOT));
                teamCount++;

                for (JsonNode pNode : tNode.path("players")) {
                    String nickname = pNode.path("nickname").asText();
                    if (nickname.isEmpty()) {
                        continue;
                    }

                    JsonNode streams = pNode.path("streams");
                    Player player = Player.builder()
                            .team(team)
                            .nickname(nickname)
                            .realName(pNode.path("realName").asText(nickname))
                            .role(pNode.path("role").asText("Player"))
                            .country(region)
                            .chzzkUrl(textOrNull(streams, "chzzk"))
                            .youtubeUrl(textOrNull(streams, "youtube"))
                            .soopUrl(textOrNull(streams, "soop"))
                            .isActive(true)
                            .build();

                    applySettingAndGears(player, pNode);
                    playerRepository.save(player);
                    playerCount++;
                }
            }

            log.info("=== 검증 시드 적재 완료 [{}]: {}개 팀, {}명 선수 ===",
                    seedPath, teamCount, playerCount);
        } catch (Exception e) {
            log.error("검증 시드 로딩 실패 [{}]: {}", seedPath, e.getMessage(), e);
        }
    }

    private void loadLegacyOfficialTeams(Set<String> loadedTeamNames) {
        File jsonFile = resolveDataFile("primary_data/official_teams_and_rosters.json");
        if (jsonFile == null) {
            log.warn("primary_data/official_teams_and_rosters.json 파일을 찾을 수 없습니다.");
            return;
        }

        log.info("=== primary_data/official_teams_and_rosters.json 기반 전체 팀/선수 전수 DB 적재 시작 ===");
        try {
            JsonNode root = objectMapper.readTree(jsonFile);
            if (!root.isArray()) {
                return;
            }

            int teamCount = 0;
            int playerCount = 0;
            int skipped = 0;

            for (JsonNode tNode : root) {
                String name = tNode.path("name").asText();

                // Team.name 이 unique 제약이라 중복 적재 시 제약 위반이 난다.
                if (loadedTeamNames.contains(name.toLowerCase(Locale.ROOT))) {
                    skipped++;
                    continue;
                }

                String region = tNode.path("region").asText("KR");
                String league = tNode.path("league").asText("PWS");

                Team team = Team.builder()
                        .name(name)
                        .region(region)
                        .tag(tNode.path("tag").asText(null))
                        .league(league)
                        .logoUrl(tNode.path("logoUrl").asText(""))
                        .description(tNode.path("description").asText(""))
                        .foundedYear(2019)
                        .coach("Official Coach")
                        .achievements(league + " Official Roster")
                        .build();

                teamRepository.save(team);
                loadedTeamNames.add(name.toLowerCase(Locale.ROOT));
                teamCount++;

                JsonNode playersNode = tNode.path("players");
                if (playersNode.isArray()) {
                    for (JsonNode pNode : playersNode) {
                        String nickname = pNode.path("nickname").asText();

                        JsonNode streams = pNode.path("streams");
                        Player player = Player.builder()
                                .team(team)
                                .nickname(nickname)
                                .realName(pNode.path("realName").asText(nickname))
                                .role(pNode.path("role").asText("Player"))
                                .country(region)
                                    .chzzkUrl(textOrNull(streams, "chzzk"))
                                .youtubeUrl(textOrNull(streams, "youtube"))
                                .soopUrl(textOrNull(streams, "soop"))
                                .isActive(true)
                                .build();

                        // 검증 시드와 같은 규칙을 쓴다. 기본값을 지어내지 않는다 —
                        // 예전에는 여기서 296명 전원에게 800/30/FOV90 과 장비 5종을 찍어 넣었다.
                        applySettingAndGears(player, pNode);
                        playerRepository.save(player);
                        playerCount++;
                    }
                }
            }
            log.info("=== 공식 API 추출 데이터 DB 적재 완료: 총 {}개 팀, 총 {}명 선수 (PWS 검증 데이터와 중복되어 건너뛴 팀 {}개) ===",
                    teamCount, playerCount, skipped);
        } catch (Exception e) {
            log.error("시드 데이터 로딩 실패: {}", e.getMessage(), e);
        }
    }


    /**
     * 시드의 setting/gears 를 선수에 붙인다.
     *
     * 시드에 있는 값만 채운다 — **기본값을 지어내지 않는다.** 예전에는 이 자리에서
     * 800 DPI, 감도 30, FOV 90, 마우스/키보드/헤드셋/모니터를 전원에게 찍어 넣었고,
     * 화면에는 실측값처럼 보였다. 없는 값은 null 로 두면 모달이 '미등록' 을 그린다.
     *
     * 시드 형식:
     * <pre>
     * {
     *   "nickname": "...",
     *   "setting": { "mouseDpi": 800, "generalSens": 47, "fov": 103,
     *                "resolution": "1920x1080", ... },
     *   "gears": [ { "category": "MOUSE", "name": "...", "brand": "...",
     *                "imageUrl": "...", "purchaseLink": "..." } ]
     * }
     * </pre>
     */
    private void applySettingAndGears(Player player, JsonNode pNode) {
        JsonNode s = pNode.path("setting");

        PlayerSetting setting = PlayerSetting.builder()
                .player(player)
                .mouseDpi(intOrNull(s, "mouseDpi"))
                .generalSens(doubleOrNull(s, "generalSens"))
                .aimingSens(doubleOrNull(s, "aimingSens"))
                .adsSens(doubleOrNull(s, "adsSens"))
                .scope2xSens(doubleOrNull(s, "scope2xSens"))
                .scope3xSens(doubleOrNull(s, "scope3xSens"))
                .scope4xSens(doubleOrNull(s, "scope4xSens"))
                .scope6xSens(doubleOrNull(s, "scope6xSens"))
                .scope8xSens(doubleOrNull(s, "scope8xSens"))
                .verticalMultiplier(doubleOrNull(s, "verticalMultiplier"))
                .fov(intOrNull(s, "fov"))
                .resolution(textOrNull(s, "resolution"))
                .screenMode(textOrNull(s, "screenMode"))
                .renderScale(intOrNull(s, "renderScale"))
                .build();
        player.setSetting(setting);

        for (JsonNode g : pNode.path("gears")) {
            String category = textOrNull(g, "category");
            String name = textOrNull(g, "name");
            // category/name 은 엔티티에서 NOT NULL 이다. 하나라도 비면 넣지 않는다.
            if (category == null || name == null) {
                log.warn("{}: category/name 이 없는 장비 항목을 건너뜁니다.", player.getNickname());
                continue;
            }
            player.addGear(PlayerGear.builder()
                    .player(player)
                    .category(category.toUpperCase(Locale.ROOT))
                    .name(name)
                    .brand(textOrNull(g, "brand"))
                    .imageUrl(textOrNull(g, "imageUrl"))
                    .purchaseLink(textOrNull(g, "purchaseLink"))
                    .sourceUrl(textOrNull(g, "sourceUrl"))
                    .collectedAt(textOrNull(g, "collectedAt"))
                    .build());
        }
    }

    private static Integer intOrNull(JsonNode node, String field) {
        JsonNode v = node.path(field);
        return v.isMissingNode() || v.isNull() ? null : v.asInt();
    }

    private static Double doubleOrNull(JsonNode node, String field) {
        JsonNode v = node.path(field);
        return v.isMissingNode() || v.isNull() ? null : v.asDouble();
    }

    private static String textOrNull(JsonNode node, String field) {
        JsonNode v = node.path(field);
        if (v.isMissingNode() || v.isNull()) {
            return null;
        }
        String text = v.asText().trim();
        return text.isEmpty() ? null : text;
    }

    private File resolveDataFile(String relativePath) {
        File file = new File(relativePath);
        if (file.exists()) {
            return file;
        }
        file = new File("../" + relativePath);
        return file.exists() ? file : null;
    }
}
