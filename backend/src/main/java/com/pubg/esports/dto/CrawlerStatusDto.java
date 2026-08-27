package com.pubg.esports.dto;

import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class CrawlerStatusDto {
    private boolean success;
    private String message;
    private String target;
    private int updatedCount;
    private LocalDateTime timestamp;
}
