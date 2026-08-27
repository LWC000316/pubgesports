package com.pubg.esports.dto;

import com.pubg.esports.domain.PlayerHighlight;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class HighlightDto {
    private Long id;
    private String title;
    private String videoUrl;
    private String tournament;

    public static HighlightDto from(PlayerHighlight highlight) {
        return HighlightDto.builder()
                .id(highlight.getId())
                .title(highlight.getTitle())
                .videoUrl(highlight.getVideoUrl())
                .tournament(highlight.getTournament())
                .build();
    }
}
