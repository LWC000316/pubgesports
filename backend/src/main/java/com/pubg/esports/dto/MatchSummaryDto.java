package com.pubg.esports.dto;

import lombok.Builder;
import lombok.Getter;

/**
 * 매치로그 목록의 한 줄. 지도에 그릴 본문(수백 KB)은 빼고 고르는 데 필요한 것만.
 *
 * 경기를 "1경기 2경기" 로 세려면 **순서를 알아야 한다.** 파일 이름은 경기 UUID 라
 * 정렬해도 순서가 아니다 — PGS 9 결승의 `15b203fc` 는 8/23 마지막 경기인데 UUID
 * 순으로는 맨 앞이었다. 순서의 근거는 공식 API 의 `createdAt` 이고
 * `_order.json` 에 적혀 있다. 그것이 없는 단계는 {@code startedAt} 이 비고,
 * 화면은 번호 대신 지도 이름만 보여 준다.
 */
@Getter
@Builder
public class MatchSummaryDto {

    private String id;
    /** 경기 시작 시각(ISO). 순서를 아는 경기만 값이 있다. */
    private String startedAt;
    /** 사람이 읽는 맵 이름 (Erangel, Miramar …). */
    private String map;
    private int duration;
    private int kills;
    /** 치킨을 먹은 팀. 킬 기록에 한 번도 나오지 않은 팀이 정확히 하나다. */
    private String winner;
}
