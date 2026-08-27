package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "tournament_player_stats")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class TournamentPlayerStat {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "tournament_id", nullable = false)
    private Tournament tournament;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    private Player player;

    private Integer rank;               // 킬/스탯 순위
    private Integer kills;              // 킬 수
    private Double damage;              // 대미지
    private Integer knocks;             // 기절(DBNO) 수
    private Integer assists;            // 어시스트
    private Double headshotRate;        // 헤드샷 비율 (%)
    private Double survivalTimeAvg;     // 평균 생존 시간 (초)
    private Double twireRating;         // Twire Rating (e.g. 1.25)

    @Builder
    public TournamentPlayerStat(Tournament tournament, Player player, Integer rank, Integer kills,
                                Double damage, Integer knocks, Integer assists, Double headshotRate,
                                Double survivalTimeAvg, Double twireRating) {
        this.tournament = tournament;
        this.player = player;
        this.rank = rank;
        this.kills = kills;
        this.damage = damage;
        this.knocks = knocks;
        this.assists = assists;
        this.headshotRate = headshotRate;
        this.survivalTimeAvg = survivalTimeAvg;
        this.twireRating = twireRating;
    }
}
