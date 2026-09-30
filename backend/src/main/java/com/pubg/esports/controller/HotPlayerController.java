package com.pubg.esports.controller;

import com.pubg.esports.dto.HotPlayerDto;
import com.pubg.esports.service.HotPlayerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/players")
@RequiredArgsConstructor
public class HotPlayerController {

    private final HotPlayerService hotPlayerService;

    /** HOT 탭 목록. 조회수 순, 없으면 초기 순위 순. */
    @GetMapping("/hot")
    public List<HotPlayerDto> getHotPlayers(@RequestParam(defaultValue = "12") int limit) {
        return hotPlayerService.getHotPlayers(Math.min(Math.max(limit, 1), 50));
    }

    /** 선수 상세를 열 때 호출한다. 응답 본문은 필요 없다. */
    @PostMapping("/{id}/view")
    public ResponseEntity<Void> recordView(@PathVariable Long id) {
        hotPlayerService.recordView(id);
        return ResponseEntity.noContent().build();
    }
}
