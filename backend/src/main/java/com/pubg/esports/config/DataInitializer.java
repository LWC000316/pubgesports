package com.pubg.esports.config;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pubg.esports.domain.*;
import com.pubg.esports.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.io.File;
import java.util.HashSet;
import java.util.Locale;
import java.util.Set;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final TeamRepository teamRepository;
    private final PlayerRepository playerRepository;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    @Transactional
    public void run(String... args) {
        Set<String> loadedTeamNames = new HashSet<>();

        // 검증된 PWS 데이터를 먼저 적재한다. 아래 레거시 파일의 PWS 항목은
        // 로고가 플레이스홀더라 덮어쓰면 안 되므로 순서가 중요하다.
        loadVerifiedPwsTeams(loadedTeamNames);
        loadLegacyOfficialTeams(loadedTeamNames);
    }

    private void loadVerifiedPwsTeams(Set<String> loadedTeamNames) {
        File jsonFile = resolveDataFile("primary_data/pws2_teams_verified.json");
        if (jsonFile == null) {
            log.warn("primary_data/pws2_teams_verified.json 파일을 찾을 수 없어 PWS 검증 데이터 적재를 건너뜁니다.");
            return;
        }

        log.info("=== 검증된 PWS 팀 데이터 적재 시작 ===");
        try {
            JsonNode root = objectMapper.readTree(jsonFile);
            if (!root.isArray()) {
                log.warn("pws2_teams_verified.json 의 최상위가 배열이 아닙니다.");
                return;
            }

            int teamCount = 0;
            int playerCount = 0;
            int trophyCount = 0;

            for (JsonNode tNode : root) {
                String name = tNode.path("name").asText();
                if (name.isEmpty()) {
                    continue;
                }

                String region = tNode.path("region").asText("KR");

                // 템플릿 문자열로 채우지 않는다. 시드에 없는 값은 비워 둔다.
                Team team = Team.builder()
                        .name(name)
                        .region(region)
                        .tag(tNode.path("tag").asText(null))
                        .seedType(tNode.path("seedType").asText(null))
                        .league(tNode.path("league").asText("PWS"))
                        .logoUrl(tNode.path("logoUrl").asText(""))
                        .build();

                for (JsonNode trNode : tNode.path("trophies")) {
                    team.addTrophy(TeamTrophy.builder()
                            .team(team)
                            .name(trNode.path("name").asText())
                            .count(trNode.path("count").asInt(0))
                            .build());
                    trophyCount++;
                }

                teamRepository.save(team);
                loadedTeamNames.add(name.toLowerCase(Locale.ROOT));
                teamCount++;

                for (JsonNode pNode : tNode.path("players")) {
                    String nickname = pNode.path("nickname").asText();
                    if (nickname.isEmpty()) {
                        continue;
                    }

                    Player player = Player.builder()
                            .team(team)
                            .nickname(nickname)
                            .realName(pNode.path("realName").asText(nickname))
                            .role(pNode.path("role").asText("Player"))
                            .country(region)
                            .isActive(true)
                            .build();

                    // 시드에 있는 값만 채운다. fov/해상도 등은 실측값이 없으므로 null 로 둔다.
                    PlayerSetting setting = PlayerSetting.builder()
                            .player(player)
                            .mouseDpi(pNode.path("mouseDpi").isMissingNode() ? null : pNode.path("mouseDpi").asInt())
                            .generalSens(pNode.path("generalSens").isMissingNode() ? null : pNode.path("generalSens").asDouble())
                            .build();
                    player.setSetting(setting);

                    String mouseName = pNode.path("mouseName").asText("");
                    if (!mouseName.isEmpty()) {
                        player.addGear(PlayerGear.builder()
                                .player(player)
                                .category("MOUSE")
                                .name(mouseName)
                                .build());
                    }

                    playerRepository.save(player);
                    playerCount++;
                }
            }

            log.info("=== PWS 검증 데이터 적재 완료: {}개 팀, {}명 선수, 트로피 {}건 ===",
                    teamCount, playerCount, trophyCount);
        } catch (Exception e) {
            log.error("PWS 검증 시드 데이터 로딩 실패: {}", e.getMessage(), e);
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
                        String realName = pNode.path("realName").asText("Pro " + nickname);
                        String role = pNode.path("role").asText("Player");
                        int dpi = pNode.path("mouseDpi").asInt(800);
                        double genSens = pNode.path("generalSens").asDouble(30.0);

                        Player player = Player.builder()
                                .team(team)
                                .nickname(nickname)
                                .realName(realName)
                                .role(role)
                                .country(region.equals("KR") ? "KR" : region.equals("CN") ? "CN" : region.equals("AMER") ? "US" : "EU")
                                .profileImageUrl("https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80")
                                .isActive(true)
                                .build();

                        PlayerSetting setting = PlayerSetting.builder()
                                .player(player)
                                .mouseDpi(dpi)
                                .generalSens(genSens)
                                .aimingSens(genSens)
                                .adsSens(genSens)
                                .verticalMultiplier(1.0)
                                .fov(90)
                                .resolution("1920x1080")
                                .screenMode("전체 화면")
                                .renderScale(100)
                                .build();

                        player.setSetting(setting);

                        player.addGear(PlayerGear.builder().player(player).category("MOUSE").name(pNode.path("mouseName").asText("Logitech G PRO X SUPERLIGHT 2")).brand("Logitech").build());
                        player.addGear(PlayerGear.builder().player(player).category("MOUSEPAD").name(pNode.path("mousepadName").asText("Artisan Zero Soft")).brand("Artisan").build());
                        player.addGear(PlayerGear.builder().player(player).category("KEYBOARD").name(pNode.path("keyboardName").asText("Wooting 60HE")).brand("Wooting").build());
                        player.addGear(PlayerGear.builder().player(player).category("HEADSET").name(pNode.path("headsetName").asText("Bose QC20")).brand("Bose").build());
                        player.addGear(PlayerGear.builder().player(player).category("MONITOR").name(pNode.path("monitorName").asText("BenQ XL2566K (360Hz)")).brand("BenQ").build());

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

    private File resolveDataFile(String relativePath) {
        File file = new File(relativePath);
        if (file.exists()) {
            return file;
        }
        file = new File("../" + relativePath);
        return file.exists() ? file : null;
    }
}
