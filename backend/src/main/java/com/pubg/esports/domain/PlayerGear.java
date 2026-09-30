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

    /** 이 장비 정보를 가져온 글의 주소. 출처가 어긋날 때 되짚을 수 있어야 한다. */
    private String sourceUrl;

    /** 그 글이 밝힌 기준일 (YYYY-MM-DD). 글 작성일이 아니라 본문의 "N월 N일 기준". */
    private String collectedAt;

    @Builder
    public PlayerGear(Player player, String category, String name, String brand, String imageUrl,
                      String purchaseLink, String sourceUrl, String collectedAt) {
        this.player = player;
        this.category = category;
        this.name = name;
        this.brand = brand;
        this.imageUrl = imageUrl;
        this.purchaseLink = purchaseLink;
        this.sourceUrl = sourceUrl;
        this.collectedAt = collectedAt;
    }
}
