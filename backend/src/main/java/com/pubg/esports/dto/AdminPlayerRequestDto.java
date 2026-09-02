package com.pubg.esports.dto;

import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
public class AdminPlayerRequestDto {
    private Long teamId;
    private String nickname;
    private String realName;
    private String role;
    private String country;
    private String profileImageUrl;
    private String chzzkUrl;
    private String youtubeUrl;
    private String soopUrl;

    // 세팅
    private Integer mouseDpi;
    private Double generalSens;
    private Double aimingSens;
    private Double adsSens;
    private Double verticalMultiplier;
    private Integer fov;
    private String resolution;

    // 기어
    private List<GearDto> gears;
}
