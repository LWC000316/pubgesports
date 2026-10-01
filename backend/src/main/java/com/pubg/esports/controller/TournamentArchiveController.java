package com.pubg.esports.controller;

import com.pubg.esports.dto.TournamentArchiveDto;
import com.pubg.esports.service.TournamentArchiveService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 대회 아카이브. `/api/tournaments/archive` 아래에 둔다 —
 * 기존 TournamentController 의 `/api/tournaments/{id}` 와 경로가 겹치지 않게 하기 위해서다.
 */
@RestController
@RequestMapping("/api/tournaments/archive")
@RequiredArgsConstructor
public class TournamentArchiveController {

    private final TournamentArchiveService tournamentArchiveService;

    /** 목록. category 는 global / regional / scrim, 없으면 전부. */
    @GetMapping
    public List<TournamentArchiveDto> list(
            @RequestParam(required = false) String category) {
        return tournamentArchiveService.list(category);
    }

    /** 대회 하나의 순위표와 선수 기록. */
    @GetMapping("/{id}")
    public ResponseEntity<TournamentArchiveDto> get(@PathVariable String id) {
        TournamentArchiveDto dto = tournamentArchiveService.get(id);
        return dto == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(dto);
    }
}
