package com.pubg.esports.dto;

import com.pubg.esports.domain.Player;
import com.pubg.esports.domain.Team;
import lombok.Builder;
import lombok.Getter;

import java.util.List;
import java.util.stream.Collectors;

/**
 * PE 탭 팀 카드 전용 뷰 DTO.
 * 필드명을 프론트엔드가 읽는 이름(logo, roster, dpi, sens, mouse)에 맞춰 내보낸다.
 */
@Getter
@Builder
public class TeamCardDto {

    private Long id;
    private String name;
    private String tag;
    private String seedType;
    private String logo;
    private String league;
    private String region;
    private List<TrophyDto> trophies;
    private List<RosterPlayerDto> roster;

    public static TeamCardDto from(Team team) {
        return TeamCardDto.builder()
                .id(team.getId())
                .name(team.getName())
                .tag(team.getTag())
                .seedType(team.getSeedType())
                .logo(team.getLogoUrl())
                .league(team.getLeague())
                .region(team.getRegion())
                .trophies(team.getTrophies().stream()
                        .map(t -> TrophyDto.builder()
                                .name(t.getName())
                                .count(t.getCount())
                                .build())
                        .collect(Collectors.toList()))
                .roster(team.getPlayers().stream()
                        .map(RosterPlayerDto::from)
                        .collect(Collectors.toList()))
                .build();
    }

    @Getter
    @Builder
    public static class TrophyDto {
        private String name;
        private int count;
    }

    @Getter
    @Builder
    public static class RosterPlayerDto {
        private Long id;
        private String nickname;
        private String realName;
        private String role;
        private Integer dpi;
        private Double sens;
        private String mouse;

        public static RosterPlayerDto from(Player player) {
            Integer dpi = player.getSetting() != null ? player.getSetting().getMouseDpi() : null;
            Double sens = player.getSetting() != null ? player.getSetting().getGeneralSens() : null;
            String mouse = player.getGears().stream()
                    .filter(g -> "MOUSE".equalsIgnoreCase(g.getCategory()))
                    .map(g -> g.getName())
                    .findFirst()
                    .orElse(null);

            return RosterPlayerDto.builder()
                    .id(player.getId())
                    .nickname(player.getNickname())
                    .realName(player.getRealName())
                    .role(player.getRole())
                    .dpi(dpi)
                    .sens(sens)
                    .mouse(mouse)
                    .build();
        }
    }
}
