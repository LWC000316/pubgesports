package com.pubg.esports.controller;

import com.pubg.esports.dto.HeatMapSummaryDto;
import com.pubg.esports.service.HeatService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 히트엔딩. 한 경기 복기가 아니라 **여러 경기를 모아 센 값**이다 —
 * 어디서 끝나고, 어디로 내리고, 어디서 죽는가.
 */
@RestController
@RequestMapping("/api/heat")
@RequiredArgsConstructor
public class HeatController {

    private final HeatService heatService;

    @GetMapping
    public List<HeatMapSummaryDto> maps() {
        return heatService.listMaps();
    }

    @GetMapping(value = "/{map}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> get(@PathVariable String map) {
        String json = heatService.read(map);
        return json == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(json);
    }
}
