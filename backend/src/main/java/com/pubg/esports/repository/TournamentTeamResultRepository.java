package com.pubg.esports.repository;

import com.pubg.esports.domain.TournamentTeamResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface TournamentTeamResultRepository extends JpaRepository<TournamentTeamResult, Long> {
    
    @Query("SELECT r FROM TournamentTeamResult r JOIN FETCH r.team WHERE r.tournament.id = :tournamentId ORDER BY r.rank ASC")
    List<TournamentTeamResult> findByTournamentIdOrderByRankAsc(@Param("tournamentId") Long tournamentId);
}
