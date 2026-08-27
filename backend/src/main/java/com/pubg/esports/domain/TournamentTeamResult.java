package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "tournament_team_results")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class TournamentTeamResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "tournament_id", nullable = false)
    private Tournament tournament;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id", nullable = false)
    private Team team;

    private Integer rank;               // 최종 순위 (1~16)
    private Integer totalPoints;        // 총점
    private Integer killPoints;         // 킬 점수
    private Integer placementPoints;    // 순위 점수
    private Integer wwcdCount;          // 치킨 횟수 (WWCD)
    private Integer matchesPlayed;      // 진행 경기 수
    private String prize;               // 획득 상금

    @Builder
    public TournamentTeamResult(Tournament tournament, Team team, Integer rank, Integer totalPoints,
                                Integer killPoints, Integer placementPoints, Integer wwcdCount,
                                Integer matchesPlayed, String prize) {
        this.tournament = tournament;
        this.team = team;
        this.rank = rank;
        this.totalPoints = totalPoints;
        this.killPoints = killPoints;
        this.placementPoints = placementPoints;
        this.wwcdCount = wwcdCount;
        this.matchesPlayed = matchesPlayed;
        this.prize = prize;
    }
}
