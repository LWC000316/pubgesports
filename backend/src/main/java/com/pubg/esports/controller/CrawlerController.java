package com.pubg.esports.controller;

import com.pubg.esports.dto.CrawlerStatusDto;
import com.pubg.esports.service.CrawlerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/crawler")
@RequiredArgsConstructor
public class CrawlerController {

    private final CrawlerService crawlerService;

    @PostMapping("/trigger/player/{nickname}")
    public ResponseEntity<CrawlerStatusDto> triggerPlayerCrawl(@PathVariable String nickname) {
        return ResponseEntity.ok(crawlerService.crawlPlayerInfo(nickname));
    }

    @PostMapping("/trigger/all")
    public ResponseEntity<CrawlerStatusDto> triggerAllCrawl() {
        return ResponseEntity.ok(crawlerService.crawlAllPlayers());
    }
}
