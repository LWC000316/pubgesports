package com.pubg.esports.repository;

import com.pubg.esports.domain.Team;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

public interface TeamRepository extends JpaRepository<Team, Long> {
    Optional<Team> findByNameIgnoreCase(String name);

    // seedType 이 있는 팀 = 검증된 대회 참가 명단. 레거시 official_teams_and_rosters.json 에도
    // league="PWS" 인 팀이 25개 있지만 로고가 플레이스홀더이고 시드 구분이 없어 제외한다.
    //
    // league 는 항상 non-null 로 받는다. nullable 파라미터를 바인딩하면
    // PostgreSQL 드라이버가 bytea 로 추론해 쿼리가 깨진다 (PlayerRepository 와 동일한 이유).
    @Query("SELECT DISTINCT t FROM Team t LEFT JOIN FETCH t.players "
            + "WHERE UPPER(t.league) = UPPER(:league) AND t.seedType IS NOT NULL ORDER BY t.id ASC")
    List<Team> findByLeagueWithPlayers(@Param("league") String league);
}
