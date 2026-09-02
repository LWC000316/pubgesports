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
@CrossOrigin(origins = "*")
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
