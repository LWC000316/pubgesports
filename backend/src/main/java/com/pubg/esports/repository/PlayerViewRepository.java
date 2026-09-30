package com.pubg.esports.repository;

import com.pubg.esports.domain.PlayerView;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface PlayerViewRepository extends JpaRepository<PlayerView, Long> {

    Optional<PlayerView> findByLeagueAndTeamNameAndNicknameAndPeriod(
            String league, String teamName, String nickname, String period);
}
