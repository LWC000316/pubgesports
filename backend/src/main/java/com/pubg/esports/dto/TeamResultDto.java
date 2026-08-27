package com.pubg.esports.dto;

import com.pubg.esports.domain.TournamentTeamResult;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class TeamResultDto {
    private Long id;
    private Integer rank;
    private Long teamId;
    private String teamName;
    private String teamRegion;
    private String teamLogoUrl;
    private Integer totalPoints;
    private Integer killPoints;
    private Integer placementPoints;
    private Integer wwcdCount;
    private Integer matchesPlayed;
    private String prize;

    public static TeamResultDto from(TournamentTeamResult result) {
        return TeamResultDto.builder()
                .id(result.getId())
                .rank(result.getRank())
                .teamId(result.getTeam().getId())
                .teamName(result.getTeam().getName())
                .teamRegion(result.getTeam().getRegion())
                .teamLogoUrl(result.getTeam().getLogoUrl())
                .totalPoints(result.getTotalPoints())
                .killPoints(result.getKillPoints())
                .placementPoints(result.getPlacementPoints())
                .wwcdCount(result.getWwcdCount())
                .matchesPlayed(result.getMatchesPlayed())
                .prize(result.getPrize())
                .build();
    }
}
