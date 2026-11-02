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
        // **없는 선수는 404 다.** 예외를 그대로 올리면 500 이 나가는데, 그건
        // 서버가 고장났다는 뜻이라 거짓이다. 방금 걷어낸 대회 엔드포인트가
        // 똑같은 이유로 늘 500 을 내고 있었다.
        PlayerDetailResponseDto found = playerService.getPlayerDetail(id);
        return found == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(found);
    }

    @GetMapping("/players/nickname/{nickname}")
    public ResponseEntity<PlayerDetailResponseDto> getPlayerByNickname(@PathVariable String nickname) {
        PlayerDetailResponseDto found = playerService.getPlayerByNickname(nickname);
        return found == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(found);
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
