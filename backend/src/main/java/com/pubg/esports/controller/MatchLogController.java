package com.pubg.esports.controller;

import com.pubg.esports.dto.MatchSummaryDto;
import com.pubg.esports.service.MatchLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 매치로그. 선수 이동 경로·자기장·킬 지점.
 * 파일이 경기당 수백 KB 라 메모리에 들고 있지 않고 요청 때 읽어 그대로 흘려보낸다.
 */
@RestController
@RequestMapping("/api/tournaments/archive/{tournamentId}/matches")
@RequiredArgsConstructor
public class MatchLogController {

    private final MatchLogService matchLogService;

    /** 그 대회에서 매치로그를 가진 경기 목록. 경기 순서대로. */
    @GetMapping
    public List<MatchSummaryDto> list(@PathVariable String tournamentId) {
        return matchLogService.listMatches(tournamentId);
    }

    @GetMapping(value = "/{matchId}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> get(@PathVariable String tournamentId,
                                      @PathVariable String matchId) {
        String json = matchLogService.read(tournamentId, matchId);
        return json == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(json);
    }
}
