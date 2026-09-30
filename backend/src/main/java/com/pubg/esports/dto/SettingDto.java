package com.pubg.esports.dto;

import com.pubg.esports.domain.PlayerSetting;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class SettingDto {
    private Integer mouseDpi;
    private Double generalSens;
    private Double aimingSens;
    private Double adsSens;
    private Double scope2xSens;
    private Double scope3xSens;
    private Double scope4xSens;
    private Double scope6xSens;
    private Double scope8xSens;
    private Double verticalMultiplier;
    private Integer fov;
    private String resolution;
    private String screenMode;
    private Integer renderScale;

    // 계산된 eDPI (DPI * 일반 감도)
    public Double getEdpi() {
        if (mouseDpi != null && generalSens != null) {
            return mouseDpi * generalSens;
        }
        return null;
    }

    public static SettingDto from(PlayerSetting setting) {
        return SettingDto.builder()
                .mouseDpi(setting.getMouseDpi())
                .generalSens(setting.getGeneralSens())
                .aimingSens(setting.getAimingSens())
                .adsSens(setting.getAdsSens())
                .scope2xSens(setting.getScope2xSens())
                .scope3xSens(setting.getScope3xSens())
                .scope4xSens(setting.getScope4xSens())
                .scope6xSens(setting.getScope6xSens())
                .scope8xSens(setting.getScope8xSens())
                .verticalMultiplier(setting.getVerticalMultiplier())
                .fov(setting.getFov())
                .resolution(setting.getResolution())
                .screenMode(setting.getScreenMode())
                .renderScale(setting.getRenderScale())
                .build();
    }
}
