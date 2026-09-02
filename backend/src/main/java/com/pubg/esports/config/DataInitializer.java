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
import java.util.ArrayList;
import java.util.List;

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
        log.info("=== primary_data/official_teams_and_rosters.json 기반 전체 팀/선수 전수 DB 적재 시작 ===");

        File jsonFile = new File("primary_data/official_teams_and_rosters.json");
        if (!jsonFile.exists()) {
            jsonFile = new File("../primary_data/official_teams_and_rosters.json");
        }

        if (!jsonFile.exists()) {
            log.warn("primary_data/official_teams_and_rosters.json 파일을 찾을 수 없습니다.");
            return;
        }

        try {
            JsonNode root = objectMapper.readTree(jsonFile);
            if (root.isArray()) {
                int teamCount = 0;
                int playerCount = 0;

                for (JsonNode tNode : root) {
                    String name = tNode.path("name").asText();
                    String region = tNode.path("region").asText("KR");
                    String league = tNode.path("league").asText("PWS");
                    String logoUrl = tNode.path("logoUrl").asText("");
                    String description = tNode.path("description").asText("");

                    Team team = Team.builder()
                            .name(name)
                            .region(region)
                            .league(league)
                            .logoUrl(logoUrl)
                            .description(description)
                            .foundedYear(2019)
                            .coach("Official Coach")
                            .achievements(league + " Official Roster")
                            .build();

                    teamRepository.save(team);
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
                log.info("=== 공식 API 추출 데이터 DB 적재 완료: 총 {}개 팀, 총 {}명 선수 ===", teamCount, playerCount);
            }
        } catch (Exception e) {
            log.error("시드 데이터 로딩 실패: {}", e.getMessage(), e);
        }
    }
}
