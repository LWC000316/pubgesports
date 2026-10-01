package com.pubg.esports.dto;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Builder;
import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

/**
 * 대회 아카이브 한 건. primary_data/tournaments/<id>.json 을 그대로 내보낸다.
 *
 * 비어 있는 Tournament 엔티티를 쓰지 않는 이유: 그쪽은 총점·순위점수·상금과
 * Team 외래키를 전제하는데, 이 데이터에는 점수가 없고(대회 규정마다 달라 계산하지
 * 않는다) 팀이 우리 Team 행과 항상 대응되지도 않는다. 대회 기록은 런타임에 쌓이는
 * 값이 아니라 정적 참조 자료라 LeagueSourceService 와 같은 방식으로 파일에서 읽는다.
 */
@Getter
@Builder
public class TournamentArchiveDto {

    private String id;
    private String name;
    /** global / regional / scrim */
    private String category;
    private String source;
    private String createdAt;
    private int matchCount;
    private List<String> maps;
    /** 점수를 계산하지 않은 이유 등, 화면에 그대로 보여줄 단서 */
    private String note;

    private List<StandingDto> standings;
    private List<PlayerStatDto> players;

    @Getter
    @Builder
    public static class StandingDto {
        private int rank;
        private String team;
        private String league;
        /** false 면 팀 이름을 우리 명단에서 찾지 못해 인게임 아이디 접두사를 쓴 것 */
        private boolean teamResolved;
        private int matches;
        private int kills;
        private int wwcd;
        private Integer bestRank;
        private Double avgRank;
    }

    @Getter
    @Builder
    public static class PlayerStatDto {
        private String nickname;
        private String team;
        private String league;
        private int kills;
        private double damage;
        private int matches;
    }

    /** 목록용. standings/players 를 빼고 요약만 담는다. */
    public TournamentArchiveDto toSummary() {
        return TournamentArchiveDto.builder()
                .id(id).name(name).category(category).source(source)
                .createdAt(createdAt).matchCount(matchCount).maps(maps).note(note)
                .build();
    }

    public static TournamentArchiveDto from(JsonNode doc) {
        List<String> maps = new ArrayList<>();
        for (JsonNode m : doc.path("maps")) {
            maps.add(m.asText());
        }

        List<StandingDto> standings = new ArrayList<>();
        for (JsonNode s : doc.path("standings")) {
            standings.add(StandingDto.builder()
                    .rank(s.path("rank").asInt())
                    .team(s.path("team").asText())
                    .league(text(s, "league"))
                    .teamResolved(s.path("teamResolved").asBoolean(false))
                    .matches(s.path("matches").asInt())
                    .kills(s.path("kills").asInt())
                    .wwcd(s.path("wwcd").asInt())
                    .bestRank(s.path("bestRank").isMissingNode() || s.path("bestRank").isNull()
                            ? null : s.path("bestRank").asInt())
                    .avgRank(s.path("avgRank").isMissingNode() || s.path("avgRank").isNull()
                            ? null : s.path("avgRank").asDouble())
                    .build());
        }

        List<PlayerStatDto> players = new ArrayList<>();
        for (JsonNode p : doc.path("players")) {
            players.add(PlayerStatDto.builder()
                    .nickname(p.path("nickname").asText())
                    .team(text(p, "team"))
                    .league(text(p, "league"))
                    .kills(p.path("kills").asInt())
                    .damage(p.path("damage").asDouble())
                    .matches(p.path("matches").asInt())
                    .build());
        }

        return TournamentArchiveDto.builder()
                .id(doc.path("id").asText())
                .name(doc.path("name").asText())
                .category(text(doc, "category"))
                .source(text(doc, "source"))
                .createdAt(text(doc, "createdAt"))
                .matchCount(doc.path("matchCount").asInt())
                .maps(maps)
                .note(text(doc, "note"))
                .standings(standings)
                .players(players)
                .build();
    }

    private static String text(JsonNode node, String field) {
        JsonNode v = node.path(field);
        return v.isMissingNode() || v.isNull() ? null : v.asText();
    }
}
