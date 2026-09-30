package com.pubg.esports.dto;

import com.pubg.esports.domain.PlayerGear;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class GearDto {
    private Long id;
    private String category;
    private String name;
    private String brand;
    private String imageUrl;
    private String purchaseLink;
    private String sourceUrl;
    private String collectedAt;

    public static GearDto from(PlayerGear gear) {
        return GearDto.builder()
                .id(gear.getId())
                .category(gear.getCategory())
                .name(gear.getName())
                .brand(gear.getBrand())
                .imageUrl(gear.getImageUrl())
                .purchaseLink(gear.getPurchaseLink())
                .sourceUrl(gear.getSourceUrl())
                .collectedAt(gear.getCollectedAt())
                .build();
    }
}
