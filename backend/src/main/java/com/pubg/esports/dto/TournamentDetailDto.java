package com.pubg.esports.dto;

import com.pubg.esports.domain.Tournament;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

@Getter
@Builder
public class TournamentDetailDto {
    private Long id;
    private String name;
    private String slug;
    private String tier;
    private String region;
    private LocalDate startDate;
    private LocalDate endDate;
    private String prizePool;
    private String logoUrl;
    private String location;
    private String status;

    private List<TeamResultDto> leaderboards;
    private List<PlayerStatDto> playerStats;

    public static TournamentDetailDto from(Tournament tournament) {
        List<TeamResultDto> teamResults = tournament.getTeamResults() != null ?
                tournament.getTeamResults().stream().map(TeamResultDto::from).collect(Collectors.toList()) :
                List.of();

        List<PlayerStatDto> playerStats = tournament.getPlayerStats() != null ?
                tournament.getPlayerStats().stream().map(PlayerStatDto::from).collect(Collectors.toList()) :
                List.of();

        return TournamentDetailDto.builder()
                .id(tournament.getId())
                .name(tournament.getName())
                .slug(tournament.getSlug())
                .tier(tournament.getTier())
                .region(tournament.getRegion())
                .startDate(tournament.getStartDate())
                .endDate(tournament.getEndDate())
                .prizePool(tournament.getPrizePool())
                .logoUrl(tournament.getLogoUrl())
                .location(tournament.getLocation())
                .status(tournament.getStatus().name())
                .leaderboards(teamResults)
                .playerStats(playerStats)
                .build();
    }
}
