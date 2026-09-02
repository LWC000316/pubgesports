package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "teams")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Team {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(nullable = false)
    private String region;

    private String league;

    private String logoUrl;

    @Column(length = 1000)
    private String description;

    private Integer foundedYear;

    private String coach;

    @Column(length = 1000)
    private String achievements;

    @OneToMany(mappedBy = "team", cascade = CascadeType.ALL)
    private List<Player> players = new ArrayList<>();

    @Builder
    public Team(String name, String region, String league, String logoUrl, String description, Integer foundedYear, String coach, String achievements) {
        this.name = name;
        this.region = region;
        this.league = league;
        this.logoUrl = logoUrl;
        this.description = description;
        this.foundedYear = foundedYear;
        this.coach = coach;
        this.achievements = achievements;
    }

    public void updateInfo(String name, String region, String league, String logoUrl, String description, Integer foundedYear, String coach, String achievements) {
        this.name = name;
        this.region = region;
        this.league = league;
        this.logoUrl = logoUrl;
        this.description = description;
        this.foundedYear = foundedYear;
        this.coach = coach;
        this.achievements = achievements;
    }
}
