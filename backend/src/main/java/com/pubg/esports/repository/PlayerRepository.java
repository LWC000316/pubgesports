package com.pubg.esports.repository;

import com.pubg.esports.domain.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface PlayerRepository extends JpaRepository<Player, Long> {

    Optional<Player> findByNicknameIgnoreCase(String nickname);

    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.team ORDER BY p.id ASC")
    List<Player> findAllWithTeam();

    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.team WHERE p.team.id = :teamId ORDER BY p.id ASC")
    List<Player> findByTeamIdWithTeam(@Param("teamId") Long teamId);

    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.team WHERE LOWER(p.nickname) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(p.realName) LIKE LOWER(CONCAT('%', :query, '%')) ORDER BY p.id ASC")
    List<Player> searchByQueryWithTeam(@Param("query") String query);

    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.team WHERE p.team.id = :teamId AND (LOWER(p.nickname) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(p.realName) LIKE LOWER(CONCAT('%', :query, '%'))) ORDER BY p.id ASC")
    List<Player> searchByTeamIdAndQueryWithTeam(@Param("teamId") Long teamId, @Param("query") String query);

    List<Player> findByTeamId(Long teamId);
}
