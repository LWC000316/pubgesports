package com.pubg.esports.dto;

import com.pubg.esports.domain.Player;
import lombok.Builder;
import lombok.Getter;

/**
 * HOT 탭 한 칸.
 *
 * 선수 정보는 여기서 따로 들고 있지 않고 **players 에서 가져온다.**
 * 예전 정적 HOT_PLAYERS_12 는 12명의 감도·장비를 따로 적어 뒀고 그 값이 실제와
 * 전부 달랐다 (seoul 이 800/32 로 적혀 있었으나 실제는 1600/30).
 */
@Getter
@Builder
public class HotPlayerDto {

    private Long id;
    private String nickname;
    private String realName;
    private String role;
    private String league;
    private String team;
    private String teamLogo;
    private String country;

    private Integer dpi;
    private Double sens;
    private String mouse;

    /** 이번 기간 조회수. 아직 없으면 0. */
    private long viewCount;

    /** 조회수가 없을 때의 초기 순위 근거. 조회수로 올라온 선수는 null. */
    private Integer seedRank;
    private String seedSource;

    public static HotPlayerDto from(Player player, long viewCount, Integer seedRank, String seedSource) {
        Integer dpi = player.getSetting() != null ? player.getSetting().getMouseDpi() : null;
        Double sens = player.getSetting() != null ? player.getSetting().getGeneralSens() : null;
        String mouse = player.getGears().stream()
                .filter(g -> "MOUSE".equalsIgnoreCase(g.getCategory()))
                .map(g -> g.getName())
                .findFirst()
                .orElse(null);

        return HotPlayerDto.builder()
                .id(player.getId())
                .nickname(player.getNickname())
                .realName(player.getRealName())
                .role(player.getRole())
                .league(player.getTeam() != null ? player.getTeam().getLeague() : null)
                .team(player.getTeam() != null ? player.getTeam().getName() : null)
                .teamLogo(player.getTeam() != null ? player.getTeam().getLogoUrl() : null)
                .country(player.getCountry())
                .dpi(dpi)
                .sens(sens)
                .mouse(mouse)
                .viewCount(viewCount)
                .seedRank(seedRank)
                .seedSource(seedSource)
                .build();
    }
}
