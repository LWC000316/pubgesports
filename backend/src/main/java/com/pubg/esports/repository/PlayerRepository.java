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

    /**
     * HOT 탭이 자연키(리그+팀+닉네임)로 선수를 찾을 때 쓴다.
     * players.id 는 SEED_MODE=always 재적재 때 바뀌므로 조회수의 키로 쓸 수 없다.
     */
    @Query("SELECT p FROM Player p LEFT JOIN FETCH p.team t "
         + "WHERE t.league = :league AND t.name = :teamName AND p.nickname = :nickname")
    Optional<Player> findByNaturalKey(@Param("league") String league,
                                                @Param("teamName") String teamName,
                                                @Param("nickname") String nickname);
}
