package com.pubg.esports.repository;

import com.pubg.esports.domain.PlayerSetting;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface PlayerSettingRepository extends JpaRepository<PlayerSetting, Long> {
    Optional<PlayerSetting> findByPlayerId(Long playerId);
}
