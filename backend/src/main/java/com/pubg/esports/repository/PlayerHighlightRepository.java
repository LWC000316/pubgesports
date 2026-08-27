package com.pubg.esports.repository;

import com.pubg.esports.domain.PlayerHighlight;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PlayerHighlightRepository extends JpaRepository<PlayerHighlight, Long> {
    List<PlayerHighlight> findByPlayerId(Long playerId);
}
