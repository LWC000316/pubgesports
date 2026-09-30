package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 기간별 선수 조회수.
 *
 * 선수를 **자연키(리그+팀+닉네임)로 가리킨다.** players.id 를 쓰면 SEED_MODE=always
 * 재적재 때 id 가 새로 부여돼 조회수가 엉뚱한 선수에게 붙는다.
 *
 * period 는 ISO 주차(2026-W40). 기간이 바뀌면 새 행이 쌓이므로 초기화 작업이 필요 없고
 * 지난 주 기록도 남는다.
 */
@Entity
@Table(name = "player_views",
       uniqueConstraints = @UniqueConstraint(
               name = "uk_player_views",
               columnNames = {"league", "team_name", "nickname", "period"}))
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class PlayerView {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String league;

    @Column(name = "team_name", nullable = false)
    private String teamName;

    @Column(nullable = false)
    private String nickname;

    @Column(nullable = false)
    private String period;

    @Column(name = "view_count", nullable = false)
    private long viewCount;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Builder
    public PlayerView(String league, String teamName, String nickname, String period) {
        this.league = league;
        this.teamName = teamName;
        this.nickname = nickname;
        this.period = period;
        this.viewCount = 0L;
        this.updatedAt = LocalDateTime.now();
    }

    public void increase() {
        this.viewCount++;
        this.updatedAt = LocalDateTime.now();
    }
}
