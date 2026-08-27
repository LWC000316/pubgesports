package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "player_highlights")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class PlayerHighlight {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    private Player player;

    @Column(nullable = false)
    private String title;

    @Column(nullable = false)
    private String videoUrl; // YouTube URL or Embed URL

    private String tournament; // e.g. PGC 2023, PGS 4, PWS

    @Builder
    public PlayerHighlight(Player player, String title, String videoUrl, String tournament) {
        this.player = player;
        this.title = title;
        this.videoUrl = videoUrl;
        this.tournament = tournament;
    }
}
