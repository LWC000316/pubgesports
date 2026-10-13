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
    /** PGS / PNC / EWC / PGC, 또는 지역 리그 코드 (PWS·PCL·EMEA·AMER·PTS·PVS) */
    private String series;
    /** 첫 경기가 열린 해. 화면이 연도로 묶는다 */
    private Integer year;
    /** 시리즈 안의 회차. PGS 7 의 "7". 없으면 null */
    private String edition;
    /** 단계 이름. 확인된 코드(gf·gs·fs)만 채워지고 나머지는 null */
    private String stage;
    /** id 에서 뽑은 단계 코드 원문. 이름을 모르는 단계를 구별하는 데 쓴다 */
    private String stageCode;
    private String startDate;
    /** 마지막 경기 날짜. 단계의 기간을 화면에 그대로 보여 주기 위한 것. */
    private String endDate;
    /** 리퀴피디아 문서 제목. 대회 단위 공식 이름이라 화면의 대회 카드가 이걸 쓴다 */
    private String officialName;
    /** 팀마다 뛴 경기 수가 다르면 {min,max}. 같으면 null — 합계로 줄 세워도 되는지 가른다 */
    private java.util.Map<String, Integer> matchesPerTeam;
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
        /** 순위 점수. PUBG 이스포츠 표준 배점(1위 10 … 7~8위 1, 9위 이하 0) */
        private int placementPoints;
        /** 킬 점수. 현행 규정은 1킬 1점이라 kills 와 같지만, 규정이 바뀌면 갈라진다 */
        private int killPoints;
        private int totalPoints;
        /** 매치당 평균 점수 */
        private Double avgPoints;
        private Integer bestRank;
        private Double avgRank;
    }

    @Getter
    @Builder
    public static class PlayerStatDto {
        private String nickname;
        private String team;
        private String league;
        private int matches;
        /** 종합 점수 */
        /** 0~100. 배틀로얄이 아닌 단계(TDM·아레나 등)는 null 이다 */
        private Integer overall;
        private int kills;
        private int knocks;
        private int assists;
        private int headshots;
        private int revives;
        private double damage;
        private double avgDamage;
        /** 평균 생존 시간(초) */
        private int avgSurvival;
        private double longestKill;
    }

    /** 목록용. standings/players 를 빼고 요약만 담는다. */
    public TournamentArchiveDto toSummary() {
        return TournamentArchiveDto.builder()
                .id(id).name(name).category(category).series(series).source(source)
                .createdAt(createdAt).matchCount(matchCount).maps(maps).note(note)
                .year(year).edition(edition).stage(stage).stageCode(stageCode)
                .startDate(startDate).endDate(endDate).matchesPerTeam(matchesPerTeam)
                .officialName(officialName)
                .build();
    }

    private static java.util.Map<String, Integer> matchesPerTeam(JsonNode doc) {
        JsonNode n = doc.path("matchesPerTeam");
        if (n.isMissingNode() || n.isNull()) {
            return null;
        }
        java.util.Map<String, Integer> out = new java.util.LinkedHashMap<>();
        out.put("min", n.path("min").asInt());
        out.put("max", n.path("max").asInt());
        return out;
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
                    .placementPoints(s.path("placementPoints").asInt())
                    .killPoints(s.path("killPoints").asInt())
                    .totalPoints(s.path("totalPoints").asInt())
                    .avgPoints(s.path("avgPoints").isMissingNode() || s.path("avgPoints").isNull()
                            ? null : s.path("avgPoints").asDouble())
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
                    .matches(p.path("matches").asInt())
                    .overall(p.path("overall").isMissingNode() || p.path("overall").isNull()
                            ? null : p.path("overall").asInt())
                    .kills(p.path("kills").asInt())
                    .knocks(p.path("knocks").asInt())
                    .assists(p.path("assists").asInt())
                    .headshots(p.path("headshots").asInt())
                    .revives(p.path("revives").asInt())
                    .damage(p.path("damage").asDouble())
                    .avgDamage(p.path("avgDamage").asDouble())
                    .avgSurvival(p.path("avgSurvival").asInt())
                    .longestKill(p.path("longestKill").asDouble())
                    .build());
        }

        return TournamentArchiveDto.builder()
                .id(doc.path("id").asText())
                .name(doc.path("name").asText())
                .category(text(doc, "category"))
                .series(text(doc, "series"))
                .year(doc.path("year").isMissingNode() || doc.path("year").isNull()
                        ? null : doc.path("year").asInt())
                .edition(text(doc, "edition"))
                .stage(text(doc, "stage"))
                .stageCode(text(doc, "stageCode"))
                .startDate(text(doc, "startDate"))
                .endDate(text(doc, "endDate"))
                .officialName(text(doc, "officialName"))
                .matchesPerTeam(matchesPerTeam(doc))
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
