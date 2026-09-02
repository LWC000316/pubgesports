package com.pubg.esports.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

@Getter
@Setter
@NoArgsConstructor
public class AdminTeamRequestDto {
    private String name;
    private String region;
    private String league;
    private String logoUrl;
    private String description;
    private Integer foundedYear;
    private String coach;
    private String achievements;
}
