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

    private String tag;

    // 대회 본선 진입 경로. pro = 직행 시드(파트너팀/직전 성적/Pro Seed),
    // amateur = 예선(컵·퀄리파이어) 통과. 리그마다 근거가 달라 화면 라벨은
    // PlayersTab 의 seedLabels 에서 리그별로 지정한다.
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
}
