package com.pubg.esports.controller;

import com.pubg.esports.service.PubgOfficialApiService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/tournaments")
@RequiredArgsConstructor
// CORS 는 WebConfig 가 /api/** 전체에 적용한다. 여기서 origins="*" 를 다시 선언하면
// allowCredentials(true) 와 충돌해 Spring 이 요청을 500 으로 거부한다.
public class PubgTournamentController {

    private final PubgOfficialApiService pubgOfficialApiService;

    /**
     * PWS, PCL (권역 대회) 및 PGS, PGC, PNC, EWC (세계 대회) 선별 조회
     */
    @GetMapping("/official")
    public ResponseEntity<List<Map<String, Object>>> getOfficialTournaments() {
        List<Map<String, Object>> tournaments = pubgOfficialApiService.getFilteredOfficialTournaments();
        return ResponseEntity.ok(tournaments);
    }
}
