package com.pubg.esports.controller;

import com.pubg.esports.dto.LeagueSourceDto;
import com.pubg.esports.service.LeagueSourceService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/leagues")
@RequiredArgsConstructor
public class LeagueSourceController {

    private final LeagueSourceService leagueSourceService;

    @GetMapping("/sources")
    public List<LeagueSourceDto> getSources() {
        return leagueSourceService.getAll();
    }

    @GetMapping("/{league}/source")
    public ResponseEntity<LeagueSourceDto> getSource(@PathVariable String league) {
        LeagueSourceDto dto = leagueSourceService.get(league);
        return dto == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(dto);
    }
}
