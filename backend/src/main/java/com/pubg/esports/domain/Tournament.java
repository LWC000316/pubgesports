package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "tournaments")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Tournament {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name; // e.g. PUBG Global Series 4 (PGS 4), PGC 2023, PWS 2024

    private String slug;

    private String tier; // S-Tier, A-Tier, Regional

    private String region; // GLOBAL, APAC, EMEA, AMER, KR

    private LocalDate startDate;

    private LocalDate endDate;

    private String prizePool; // e.g. $300,000

    private String logoUrl;

    private String location; // e.g. Shanghai, China

    @Enumerated(EnumType.STRING)
    private TournamentStatus status = TournamentStatus.COMPLETED;

    @OneToMany(mappedBy = "tournament", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderBy("rank ASC")
    private List<TournamentTeamResult> teamResults = new ArrayList<>();

    @OneToMany(mappedBy = "tournament", cascade = CascadeType.ALL, orphanRemoval = true)
    @OrderBy("rank ASC")
    private List<TournamentPlayerStat> playerStats = new ArrayList<>();

    @Builder
    public Tournament(String name, String slug, String tier, String region, LocalDate startDate,
                      LocalDate endDate, String prizePool, String logoUrl, String location, TournamentStatus status) {
        this.name = name;
        this.slug = slug;
        this.tier = tier;
        this.region = region;
        this.startDate = startDate;
        this.endDate = endDate;
        this.prizePool = prizePool;
        this.logoUrl = logoUrl;
        this.location = location;
        this.status = status != null ? status : TournamentStatus.COMPLETED;
    }

    public enum TournamentStatus {
        UPCOMING, ONGOING, COMPLETED
    }

    public void addTeamResult(TournamentTeamResult result) {
        this.teamResults.add(result);
    }

    public void addPlayerStat(TournamentPlayerStat stat) {
        this.playerStats.add(stat);
    }
}
