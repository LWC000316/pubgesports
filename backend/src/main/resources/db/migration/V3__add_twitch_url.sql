-- 트위치 채널 주소 칸을 추가한다.
--
-- Player 에는 chzzk/youtube/soop 만 있었다. 실제 데이터를 보고 만든 칸이 아니라
-- 한국 플랫폼만 떠올려 만든 탓이다. 리퀴피디아 선수 문서에서 방송 링크를 모아 보니
-- 170명 중 twitch 가 149명으로 가장 많았다 (youtube 85, soop 14).
ALTER TABLE players ADD COLUMN twitch_url varchar(255);
