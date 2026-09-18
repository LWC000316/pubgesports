package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.BatchSize;

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

    private String tag;

    private String seedType; // pro, amateur

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

    // players 와 동시에 fetch join 하면 MultipleBagFetchException 이 나므로 배치 로딩으로 가져온다.
    @BatchSize(size = 50)
    @OneToMany(mappedBy = "team", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<TeamTrophy> trophies = new ArrayList<>();

    @Builder
    public Team(String name, String region, String tag, String seedType, String league, String logoUrl, String description, Integer foundedYear, String coach, String achievements) {
        this.name = name;
        this.region = region;
        this.tag = tag;
        this.seedType = seedType;
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

    public void addTrophy(TeamTrophy trophy) {
        this.trophies.add(trophy);
        trophy.assignTeam(this);
    }

    public void clearTrophies() {
        this.trophies.clear();
    }
}
