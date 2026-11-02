-- 쓰지 않는 테이블을 정리한다.
--
-- 대회 탭은 `primary_data/tournaments/` 의 JSON 을 그대로 읽는다
-- (TournamentArchiveService). 점수가 공식 API 에 없어 재구성한 값이고 팀이
-- 우리 Team 행과 항상 대응되지도 않아서, 처음부터 엔티티를 쓰지 않았다.
-- 그래서 아래 세 테이블은 **한 번도 채워진 적이 없다** — 확인 시점에 전부 0행.
--
-- 비어 있는 채로 두니 `/api/tournaments/{id}` 같은 엔드포인트가 살아서 늘 빈
-- 결과를 냈다. 그쪽 엔티티·리포지토리·서비스·컨트롤러를 지우면서 테이블도
-- 같이 내린다. 남겨 두면 "언젠가 쓰는 길"처럼 보여 다음 사람을 헷갈리게 한다.
--
-- `player_highlights` 는 엔티티조차 없는 고아 테이블이다. V1 이 Hibernate 가
-- 만들던 스키마를 그대로 옮긴 것이라 그때 같이 들어왔다.
--
-- 되살릴 일이 생기면 V1 의 정의를 보고 새 마이그레이션으로 다시 만들면 된다.

DROP TABLE IF EXISTS tournament_player_stats;
DROP TABLE IF EXISTS tournament_team_results;
DROP TABLE IF EXISTS tournaments;
DROP TABLE IF EXISTS player_highlights;
