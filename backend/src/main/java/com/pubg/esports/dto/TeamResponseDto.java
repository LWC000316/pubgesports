package com.pubg.esports.dto;

import com.pubg.esports.domain.Team;
import lombok.Builder;
import lombok.Getter;

import java.util.List;
import java.util.stream.Collectors;

@Getter
@Builder
public class TeamResponseDto {
    private Long id;
    private String name;
    private String region;
    private String league;
    private String logoUrl;
    private String description;
    private Integer foundedYear;
    private String coach;
    private String achievements;
    private List<PlayerListResponseDto> players;

    public static TeamResponseDto from(Team team) {
        List<PlayerListResponseDto> playerDtos = team.getPlayers() != null ?
                team.getPlayers().stream().map(PlayerListResponseDto::from).collect(Collectors.toList()) :
                List.of();

        return TeamResponseDto.builder()
                .id(team.getId())
                .name(team.getName())
                .region(team.getRegion())
                .league(team.getLeague())
                .logoUrl(team.getLogoUrl())
                .description(team.getDescription())
                .foundedYear(team.getFoundedYear())
                .coach(team.getCoach())
                .achievements(team.getAchievements())
                .players(playerDtos)
                .build();
    }
}
