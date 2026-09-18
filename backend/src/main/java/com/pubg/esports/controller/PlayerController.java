package com.pubg.esports.controller;

import com.pubg.esports.dto.PlayerDetailResponseDto;
import com.pubg.esports.dto.PlayerListResponseDto;
import com.pubg.esports.dto.TeamCardDto;
import com.pubg.esports.dto.TeamResponseDto;
import com.pubg.esports.service.PlayerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class PlayerController {

    private final PlayerService playerService;

    @GetMapping("/players")
    public ResponseEntity<List<PlayerListResponseDto>> getPlayers(
            @RequestParam(required = false) Long teamId,
            @RequestParam(required = false) String query) {
        return ResponseEntity.ok(playerService.getPlayers(teamId, query));
    }

    @GetMapping("/players/{id}")
    public ResponseEntity<PlayerDetailResponseDto> getPlayerDetail(@PathVariable Long id) {
        return ResponseEntity.ok(playerService.getPlayerDetail(id));
    }

    @GetMapping("/players/nickname/{nickname}")
    public ResponseEntity<PlayerDetailResponseDto> getPlayerByNickname(@PathVariable String nickname) {
        return ResponseEntity.ok(playerService.getPlayerByNickname(nickname));
    }

    @GetMapping("/teams")
    public ResponseEntity<List<TeamResponseDto>> getTeams() {
        return ResponseEntity.ok(playerService.getAllTeams());
    }

    @GetMapping("/teams/cards")
    public ResponseEntity<List<TeamCardDto>> getTeamCards(
            @RequestParam(defaultValue = "PWS") String league) {
        return ResponseEntity.ok(playerService.getTeamCards(league));
    }
}
