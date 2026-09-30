package com.pubg.esports.dto;

import com.pubg.esports.domain.Player;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Getter
@Builder
public class PlayerDetailResponseDto {
    private Long id;
    private String nickname;
    private String realName;
    private String role;
    private String country;
    private String profileImageUrl;
    private String twitchUrl;
    private String chzzkUrl;
    private String youtubeUrl;
    private String soopUrl;
    private boolean isActive;
    private LocalDateTime lastCrawledAt;

    private TeamInfo team;
    private SettingDto setting;
    private List<GearDto> gears;

    @Getter
    @Builder
    public static class TeamInfo {
        private Long id;
        private String name;
        private String region;
        private String logoUrl;
    }

    public static PlayerDetailResponseDto from(Player player) {
        TeamInfo teamInfo = null;
        if (player.getTeam() != null) {
            teamInfo = TeamInfo.builder()
                    .id(player.getTeam().getId())
                    .name(player.getTeam().getName())
                    .region(player.getTeam().getRegion())
                    .logoUrl(player.getTeam().getLogoUrl())
                    .build();
        }

        SettingDto settingDto = player.getSetting() != null ? SettingDto.from(player.getSetting()) : null;
        List<GearDto> gearDtos = player.getGears().stream().map(GearDto::from).collect(Collectors.toList());

        return PlayerDetailResponseDto.builder()
                .id(player.getId())
                .nickname(player.getNickname())
                .realName(player.getRealName())
                .role(player.getRole())
                .country(player.getCountry())
                .profileImageUrl(player.getProfileImageUrl())
                .twitchUrl(player.getTwitchUrl())
                .chzzkUrl(player.getChzzkUrl())
                .youtubeUrl(player.getYoutubeUrl())
                .soopUrl(player.getSoopUrl())
                .isActive(player.isActive())
                .lastCrawledAt(player.getLastCrawledAt())
                .team(teamInfo)
                .setting(settingDto)
                .gears(gearDtos)
                .build();
    }
}
