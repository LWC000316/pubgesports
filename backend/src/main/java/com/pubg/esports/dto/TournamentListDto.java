package com.pubg.esports.dto;

import com.pubg.esports.domain.Tournament;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;

@Getter
@Builder
public class TournamentListDto {
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
    private Integer totalTeams;

    public static TournamentListDto from(Tournament tournament) {
        return TournamentListDto.builder()
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
                .totalTeams(tournament.getTeamResults() != null ? tournament.getTeamResults().size() : 0)
                .build();
    }
}
