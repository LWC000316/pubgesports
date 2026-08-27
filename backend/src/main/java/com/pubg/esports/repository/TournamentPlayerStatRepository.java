package com.pubg.esports.repository;

import com.pubg.esports.domain.TournamentPlayerStat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface TournamentPlayerStatRepository extends JpaRepository<TournamentPlayerStat, Long> {

    @Query("SELECT s FROM TournamentPlayerStat s JOIN FETCH s.player p LEFT JOIN FETCH p.team WHERE s.tournament.id = :tournamentId ORDER BY s.kills DESC, s.damage DESC")
    List<TournamentPlayerStat> findByTournamentIdOrderByKillsDesc(@Param("tournamentId") Long tournamentId);

    List<TournamentPlayerStat> findByPlayerId(Long playerId);
}
