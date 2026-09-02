package com.pubg.esports.service;

import com.pubg.esports.domain.*;
import com.pubg.esports.dto.*;
import com.pubg.esports.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class AdminService {

    private final TeamRepository teamRepository;
    private final PlayerRepository playerRepository;
    private final PlayerSettingRepository settingRepository;
    private final PlayerGearRepository gearRepository;

    @Transactional
    public Long createTeam(AdminTeamRequestDto dto) {
        Team team = Team.builder()
                .name(dto.getName())
                .region(dto.getRegion())
                .league(dto.getLeague())
                .logoUrl(dto.getLogoUrl())
                .description(dto.getDescription())
                .foundedYear(dto.getFoundedYear())
                .coach(dto.getCoach())
                .achievements(dto.getAchievements())
                .build();
        return teamRepository.save(team).getId();
    }

    @Transactional
    public void updateTeam(Long teamId, AdminTeamRequestDto dto) {
        Team team = teamRepository.findById(teamId)
                .orElseThrow(() -> new IllegalArgumentException("팀을 찾을 수 없습니다: " + teamId));
        team.updateInfo(dto.getName(), dto.getRegion(), dto.getLeague(), dto.getLogoUrl(),
                dto.getDescription(), dto.getFoundedYear(), dto.getCoach(), dto.getAchievements());
    }

    @Transactional
    public void deleteTeam(Long teamId) {
        teamRepository.deleteById(teamId);
    }

    @Transactional
    public Long createPlayer(AdminPlayerRequestDto dto) {
        Team team = null;
        if (dto.getTeamId() != null) {
            team = teamRepository.findById(dto.getTeamId()).orElse(null);
        }

        Player player = Player.builder()
                .team(team)
                .nickname(dto.getNickname())
                .realName(dto.getRealName())
                .role(dto.getRole())
                .country(dto.getCountry())
                .profileImageUrl(dto.getProfileImageUrl())
                .chzzkUrl(dto.getChzzkUrl())
                .youtubeUrl(dto.getYoutubeUrl())
                .soopUrl(dto.getSoopUrl())
                .isActive(true)
                .build();

        player.setLastCrawledAt(LocalDateTime.now());

        PlayerSetting setting = PlayerSetting.builder()
                .player(player)
                .mouseDpi(dto.getMouseDpi() != null ? dto.getMouseDpi() : 800)
                .generalSens(dto.getGeneralSens() != null ? dto.getGeneralSens() : 30.0)
                .aimingSens(dto.getAimingSens() != null ? dto.getAimingSens() : 30.0)
                .adsSens(dto.getAdsSens() != null ? dto.getAdsSens() : 30.0)
                .verticalMultiplier(dto.getVerticalMultiplier() != null ? dto.getVerticalMultiplier() : 1.0)
                .fov(dto.getFov() != null ? dto.getFov() : 90)
                .resolution(dto.getResolution() != null ? dto.getResolution() : "1920x1080")
                .screenMode("전체 화면")
                .renderScale(100)
                .build();

        player.setSetting(setting);

        if (dto.getGears() != null) {
            for (GearDto g : dto.getGears()) {
                if (g.getName() != null && !g.getName().isBlank()) {
                    player.addGear(PlayerGear.builder()
                            .player(player)
                            .category(g.getCategory())
                            .name(g.getName())
                            .brand(g.getBrand())
                            .build());
                }
            }
        }

        return playerRepository.save(player).getId();
    }

    @Transactional
    public void updatePlayer(Long playerId, AdminPlayerRequestDto dto) {
        Player player = playerRepository.findById(playerId)
                .orElseThrow(() -> new IllegalArgumentException("선수를 찾을 수 없습니다: " + playerId));

        if (dto.getTeamId() != null) {
            Team team = teamRepository.findById(dto.getTeamId()).orElse(null);
            player.setTeam(team);
        }

        player.updateProfile(dto.getNickname(), dto.getRealName(), dto.getRole(),
                dto.getCountry(), dto.getProfileImageUrl(), dto.getChzzkUrl(), dto.getYoutubeUrl(), dto.getSoopUrl());

        if (player.getSetting() != null) {
            player.getSetting().updateSetting(
                    dto.getMouseDpi(), dto.getGeneralSens(), dto.getAimingSens(),
                    dto.getAdsSens(), dto.getVerticalMultiplier(), dto.getFov(), dto.getResolution()
            );
        } else {
            PlayerSetting setting = PlayerSetting.builder()
                    .player(player)
                    .mouseDpi(dto.getMouseDpi())
                    .generalSens(dto.getGeneralSens())
                    .aimingSens(dto.getAimingSens())
                    .adsSens(dto.getAdsSens())
                    .verticalMultiplier(dto.getVerticalMultiplier())
                    .fov(dto.getFov())
                    .resolution(dto.getResolution())
                    .build();
            player.setSetting(setting);
        }

        if (dto.getGears() != null) {
            player.clearGears();
            for (GearDto g : dto.getGears()) {
                if (g.getName() != null && !g.getName().isBlank()) {
                    player.addGear(PlayerGear.builder()
                            .player(player)
                            .category(g.getCategory())
                            .name(g.getName())
                            .brand(g.getBrand())
                            .build());
                }
            }
        }

        player.setLastCrawledAt(LocalDateTime.now());
    }

    @Transactional
    public void deletePlayer(Long playerId) {
        playerRepository.deleteById(playerId);
    }
}
