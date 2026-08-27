package com.pubg.esports.repository;

import com.pubg.esports.domain.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface PlayerRepository extends JpaRepository<Player, Long> {

    Optional<Player> findByNicknameIgnoreCase(String nickname);

    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.team WHERE " +
           "(:teamId IS NULL OR p.team.id = :teamId) AND " +
           "(:query IS NULL OR LOWER(p.nickname) LIKE LOWER(CONCAT('%', :query, '%')) OR LOWER(p.realName) LIKE LOWER(CONCAT('%', :query, '%')))")
    List<Player> searchPlayers(@Param("teamId") Long teamId, @Param("query") String query);

    List<Player> findByTeamId(Long teamId);
}
