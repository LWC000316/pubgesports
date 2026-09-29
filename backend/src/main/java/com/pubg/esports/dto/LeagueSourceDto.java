package com.pubg.esports.dto;

import com.fasterxml.jackson.databind.JsonNode;
import lombok.Builder;
import lombok.Getter;

/**
 * 리그 시드가 어느 대회 문서에서 언제 수집됐는지.
 * primary_data/_sources.json 을 그대로 내보낸다.
 *
 * 화면에 "언제 기준 데이터인가" 를 표시하기 위한 것이다. 이 값이 없던 동안
 * PTS 가 5개월 지난 대회를 가리키고 있어도 아무도 알 수 없었다.
 */
@Getter
@Builder
public class LeagueSourceDto {

    private String league;
    private String page;
    private String collectedAt;
    private String tournamentStart;
    private String tournamentEnd;
    private String note;

    public static LeagueSourceDto from(String league, JsonNode node) {
        return LeagueSourceDto.builder()
                .league(league)
                .page(text(node, "page"))
                .collectedAt(text(node, "collectedAt"))
                .tournamentStart(text(node, "tournamentStart"))
                .tournamentEnd(text(node, "tournamentEnd"))
                .note(text(node, "note"))
                .build();
    }

    private static String text(JsonNode node, String field) {
        JsonNode value = node.path(field);
        return value.isMissingNode() || value.isNull() ? null : value.asText();
    }
}
