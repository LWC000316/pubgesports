package com.pubg.esports.controller;

import com.pubg.esports.dto.PlayerStatDto;
import com.pubg.esports.dto.TeamResultDto;
import com.pubg.esports.dto.TournamentDetailDto;
import com.pubg.esports.dto.TournamentListDto;
import com.pubg.esports.service.TournamentService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tournaments")
@RequiredArgsConstructor
public class TournamentController {

    private final TournamentService tournamentService;

    @GetMapping
    public ResponseEntity<List<TournamentListDto>> getTournaments() {
        return ResponseEntity.ok(tournamentService.getAllTournaments());
    }

    @GetMapping("/{id}")
    public ResponseEntity<TournamentDetailDto> getTournamentDetail(@PathVariable Long id) {
        return ResponseEntity.ok(tournamentService.getTournamentDetail(id));
    }

    @GetMapping("/slug/{slug}")
    public ResponseEntity<TournamentDetailDto> getTournamentBySlug(@PathVariable String slug) {
        return ResponseEntity.ok(tournamentService.getTournamentBySlug(slug));
    }

    @GetMapping("/{id}/leaderboard")
    public ResponseEntity<List<TeamResultDto>> getTournamentLeaderboard(@PathVariable Long id) {
        return ResponseEntity.ok(tournamentService.getTournamentLeaderboard(id));
    }

    @GetMapping("/{id}/stats")
    public ResponseEntity<List<PlayerStatDto>> getTournamentPlayerStats(@PathVariable Long id) {
        return ResponseEntity.ok(tournamentService.getTournamentPlayerStats(id));
    }
}
