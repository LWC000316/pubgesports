package com.pubg.esports.dto;

import com.pubg.esports.domain.TournamentPlayerStat;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class PlayerStatDto {
    private Long id;
    private Integer rank;
    private Long playerId;
    private String playerNickname;
    private String playerRealName;
    private String playerProfileImageUrl;
    private String playerRole;
    private String playerCountry;
    private String teamName;
    private String teamLogoUrl;
    private Integer kills;
    private Double damage;
    private Integer knocks;
    private Integer assists;
    private Double headshotRate;
    private Double survivalTimeAvg;
    private Double twireRating;

    public static PlayerStatDto from(TournamentPlayerStat stat) {
        return PlayerStatDto.builder()
                .id(stat.getId())
                .rank(stat.getRank())
                .playerId(stat.getPlayer().getId())
                .playerNickname(stat.getPlayer().getNickname())
                .playerRealName(stat.getPlayer().getRealName())
                .playerProfileImageUrl(stat.getPlayer().getProfileImageUrl())
                .playerRole(stat.getPlayer().getRole())
                .playerCountry(stat.getPlayer().getCountry())
                .teamName(stat.getPlayer().getTeam() != null ? stat.getPlayer().getTeam().getName() : null)
                .teamLogoUrl(stat.getPlayer().getTeam() != null ? stat.getPlayer().getTeam().getLogoUrl() : null)
                .kills(stat.getKills())
                .damage(stat.getDamage())
                .knocks(stat.getKnocks())
                .assists(stat.getAssists())
                .headshotRate(stat.getHeadshotRate())
                .survivalTimeAvg(stat.getSurvivalTimeAvg())
                .twireRating(stat.getTwireRating())
                .build();
    }
}
