package com.pubg.esports.dto;

import lombok.Builder;
import lombok.Getter;

/**
 * 히트엔딩 맵 목록의 한 줄.
 *
 * {@code matches} 를 반드시 같이 보여 준다 — 비켄디 15경기와 에란겔 1,198경기를
 * 같은 무게로 읽으면 거짓이 된다. 표본이 적은 맵은 아예 집계되지 않는다
 * (`ingest/build_heat.py` 의 MIN_MATCHES).
 */
@Getter
@Builder
public class HeatMapSummaryDto {

    private String map;
    private String mapLabel;
    /** 지도 그림 파일 이름. 옛 맵은 현재판 그림을 빌려 쓴다. */
    private String image;
    /** 출처를 합친 경기 수. 화면에서는 보통 출처별로 보여준다. */
    private int matches;
    /** 출처별 경기 수 — esports / competitive. */
    private java.util.Map<String, Integer> bySource;
    /** 언제부터의 경기인가 (자기장 개편일). */
    private String since;
}
