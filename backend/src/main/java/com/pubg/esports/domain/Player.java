package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "players")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Player {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "team_id")
    private Team team;

    @Column(nullable = false)
    private String nickname;

    private String realName;

    private String role; // Main Attacker, IGL, Support, Scout 등

    private String country;

    private String profileImageUrl;

    private String chzzkUrl;

    private String youtubeUrl;

    private String soopUrl;

    private boolean isActive = true;

    private java.time.LocalDateTime lastCrawledAt;

    @OneToOne(mappedBy = "player", cascade = CascadeType.ALL, orphanRemoval = true)
    private PlayerSetting setting;

    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<PlayerGear> gears = new ArrayList<>();

    @OneToMany(mappedBy = "player", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<PlayerHighlight> highlights = new ArrayList<>();

    @Builder
    public Player(Team team, String nickname, String realName, String role, String country,
                  String profileImageUrl, String chzzkUrl, String youtubeUrl, String soopUrl, boolean isActive) {
        this.team = team;
        this.nickname = nickname;
        this.realName = realName;
        this.role = role;
        this.country = country;
        this.profileImageUrl = profileImageUrl;
        this.chzzkUrl = chzzkUrl;
        this.youtubeUrl = youtubeUrl;
        this.soopUrl = soopUrl;
        this.isActive = isActive;
    }

    public void setSetting(PlayerSetting setting) {
        this.setting = setting;
    }

    public void setLastCrawledAt(java.time.LocalDateTime lastCrawledAt) {
        this.lastCrawledAt = lastCrawledAt;
    }

    public void setTeam(Team team) {
        this.team = team;
    }

    public void updateProfile(String nickname, String realName, String role, String country,
                              String profileImageUrl, String chzzkUrl, String youtubeUrl, String soopUrl) {
        this.nickname = nickname;
        this.realName = realName;
        this.role = role;
        this.country = country;
        this.profileImageUrl = profileImageUrl;
        this.chzzkUrl = chzzkUrl;
        this.youtubeUrl = youtubeUrl;
        this.soopUrl = soopUrl;
    }

    public void clearGears() {
        this.gears.clear();
    }

    public void addGear(PlayerGear gear) {
        this.gears.add(gear);
    }

    public void addHighlight(PlayerHighlight highlight) {
        this.highlights.add(highlight);
    }
}
