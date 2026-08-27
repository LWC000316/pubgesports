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
    private String logoUrl;
    private List<PlayerListResponseDto> players;

    public static TeamResponseDto from(Team team) {
        List<PlayerListResponseDto> playerDtos = team.getPlayers() != null ?
                team.getPlayers().stream().map(PlayerListResponseDto::from).collect(Collectors.toList()) :
                List.of();

        return TeamResponseDto.builder()
                .id(team.getId())
                .name(team.getName())
                .region(team.getRegion())
                .logoUrl(team.getLogoUrl())
                .players(playerDtos)
                .build();
    }
}
