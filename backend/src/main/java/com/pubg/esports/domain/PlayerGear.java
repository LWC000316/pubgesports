package com.pubg.esports.domain;

import jakarta.persistence.*;
import lombok.AccessLevel;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "player_gears")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class PlayerGear {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "player_id", nullable = false)
    private Player player;

    @Column(nullable = false)
    private String category; // MOUSE, MOUSEPAD, KEYBOARD, HEADSET, MONITOR, EARPHONE, DAC

    @Column(nullable = false)
    private String name;

    private String brand;

    private String imageUrl;

    private String purchaseLink;

    @Builder
    public PlayerGear(Player player, String category, String name, String brand, String imageUrl, String purchaseLink) {
        this.player = player;
        this.category = category;
        this.name = name;
        this.brand = brand;
        this.imageUrl = imageUrl;
        this.purchaseLink = purchaseLink;
    }
}
