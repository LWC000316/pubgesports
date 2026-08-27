package com.pubg.esports.dto;

import com.pubg.esports.domain.Player;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class PlayerListResponseDto {
    private Long id;
    private String nickname;
    private String realName;
    private String role;
    private String country;
    private String profileImageUrl;
    private String teamName;
    private String teamLogoUrl;
    private Integer mouseDpi;
    private Double generalSens;
    private String mouseName;
    private LocalDateTime lastCrawledAt;

    public static PlayerListResponseDto from(Player player) {
        Integer dpi = player.getSetting() != null ? player.getSetting().getMouseDpi() : null;
        Double generalSens = player.getSetting() != null ? player.getSetting().getGeneralSens() : null;
        String mouse = player.getGears().stream()
                .filter(g -> "MOUSE".equalsIgnoreCase(g.getCategory()))
                .map(g -> g.getName())
                .findFirst()
                .orElse(null);

        return PlayerListResponseDto.builder()
                .id(player.getId())
                .nickname(player.getNickname())
                .realName(player.getRealName())
                .role(player.getRole())
                .country(player.getCountry())
                .profileImageUrl(player.getProfileImageUrl())
                .teamName(player.getTeam() != null ? player.getTeam().getName() : null)
                .teamLogoUrl(player.getTeam() != null ? player.getTeam().getLogoUrl() : null)
                .mouseDpi(dpi)
                .generalSens(generalSens)
                .mouseName(mouse)
                .lastCrawledAt(player.getLastCrawledAt())
                .build();
    }
}
