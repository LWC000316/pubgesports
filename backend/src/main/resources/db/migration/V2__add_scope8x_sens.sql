-- 8배율 감도 칸을 추가한다.
--
-- PlayerSetting 의 배율별 감도는 2·3·4·6배율까지만 있었다. 실제 데이터를 보고
-- 만든 것이 아니라 상상해서 만든 칸이라 8배율이 빠져 있었다.
-- 2026-09-29 에 처음 들어온 실측 데이터(PUBG PRO SENS 시트, 286명)에 8배율이
-- 있어 칸을 맞춘다.
ALTER TABLE player_settings ADD COLUMN scope8x_sens double precision;
