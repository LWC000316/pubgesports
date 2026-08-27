package com.pubg.esports.repository;

import com.pubg.esports.domain.Tournament;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.Optional;

public interface TournamentRepository extends JpaRepository<Tournament, Long> {
    Optional<Tournament> findBySlug(String slug);

    @Query("SELECT t FROM Tournament t ORDER BY t.startDate DESC")
    List<Tournament> findAllOrderByStartDateDesc();
}
