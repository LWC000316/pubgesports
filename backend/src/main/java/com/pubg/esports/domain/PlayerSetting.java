package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "player_settings")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class PlayerSetting {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    private Player player;

    private Integer mouseDpi;             // e.g. 800, 1600
    private Double generalSens;           // 일반 감도
    private Double aimingSens;            // 조준 감도
    private Double adsSens;               // ADS 스코프 감도
    private Double scope2xSens;           // 2배율 감도
    private Double scope3xSens;           // 3배율 감도
    private Double scope4xSens;           // 4배율 감도
    private Double scope6xSens;           // 6배율 감도
    private Double verticalMultiplier;    // 수직 감도 배율 (e.g. 1.0, 1.2)
    private Integer fov;                  // 1인칭 시야각 (e.g. 90, 103)
    private String resolution;            // 해상도 (e.g. 1920x1080, 1728x1080)
    private String screenMode;            // 전체화면 등
    private Integer renderScale;          // 렌더링 크기 (e.g. 100, 120)

    @Builder
    public PlayerSetting(Player player, Integer mouseDpi, Double generalSens, Double aimingSens, Double adsSens,
                         Double scope2xSens, Double scope3xSens, Double scope4xSens, Double scope6xSens,
                         Double verticalMultiplier, Integer fov, String resolution, String screenMode, Integer renderScale) {
        this.player = player;
        this.mouseDpi = mouseDpi;
        this.generalSens = generalSens;
        this.aimingSens = aimingSens;
        this.adsSens = adsSens;
        this.scope2xSens = scope2xSens;
        this.scope3xSens = scope3xSens;
        this.scope4xSens = scope4xSens;
        this.scope6xSens = scope6xSens;
        this.verticalMultiplier = verticalMultiplier;
        this.fov = fov;
        this.resolution = resolution;
        this.screenMode = screenMode;
        this.renderScale = renderScale;
    }
}
