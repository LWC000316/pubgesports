package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 조회수가 쌓이기 전 HOT 탭을 채우는 초기 순위.
 * 세계대회 성적을 기준으로 사람이 정하고 `source` 에 근거를 남긴다.
 * 조회수가 쌓이면 자연히 밀려난다.
 */
@Entity
@Table(name = "hot_seeds",
       uniqueConstraints = @UniqueConstraint(
               name = "uk_hot_seeds", columnNames = {"league", "team_name", "nickname"}))
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class HotSeed {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String league;

    @Column(name = "team_name", nullable = false)
    private String teamName;

    @Column(nullable = false)
    private String nickname;

    @Column(name = "seed_rank", nullable = false)
    private int seedRank;

    @Column(length = 500)
    private String source;

    @Column(length = 500)
    private String note;

    public static HotSeed of(String league, String teamName, String nickname,
                             int seedRank, String source, String note) {
        HotSeed seed = new HotSeed();
        seed.league = league;
        seed.teamName = teamName;
        seed.nickname = nickname;
        seed.seedRank = seedRank;
        seed.source = source;
        seed.note = note;
        return seed;
    }
}
