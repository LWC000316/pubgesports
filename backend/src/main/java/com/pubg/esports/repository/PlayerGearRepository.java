package com.pubg.esports.repository;

import com.pubg.esports.domain.PlayerGear;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PlayerGearRepository extends JpaRepository<PlayerGear, Long> {
    List<PlayerGear> findByPlayerId(Long playerId);
    List<PlayerGear> findByCategoryIgnoreCase(String category);
}
