-- 장비의 출처와 기준일 칸을 추가한다.
--
-- 장비는 감도보다 자주 바뀌고 출처가 서로 어긋난다. Salute 는 유튜브 설명과
-- SOOP 공지의 마우스·키보드·패드·헤드셋이 전부 달랐다. 어디서 언제 가져왔는지를
-- 같이 남기지 않으면 나중에 어느 쪽이 맞는지 다시 확인할 방법이 없다.
ALTER TABLE player_gears ADD COLUMN source_url varchar(500);
ALTER TABLE player_gears ADD COLUMN collected_at varchar(20);
