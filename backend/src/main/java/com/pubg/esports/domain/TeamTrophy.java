package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "team_trophies")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class TeamTrophy {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id", nullable = false)
    private Team team;

    @Column(nullable = false)
    private String name; // PWS, PGC, PGS, PGI, PKL, BSC, PPM, PCS, APL, PLS, PEC

    @Column(nullable = false)
    private int count;

    @Builder
    public TeamTrophy(Team team, String name, int count) {
        this.team = team;
        this.name = name;
        this.count = count;
    }

    void assignTeam(Team team) {
        this.team = team;
    }
}
