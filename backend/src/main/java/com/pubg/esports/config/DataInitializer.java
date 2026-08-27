package com.pubg.esports.config;

import com.pubg.esports.domain.*;
import com.pubg.esports.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final TeamRepository teamRepository;
    private final PlayerRepository playerRepository;
    private final TournamentRepository tournamentRepository;
    private final TournamentTeamResultRepository teamResultRepository;
    private final TournamentPlayerStatRepository playerStatRepository;

    @Override
    @Transactional
    public void run(String... args) {
        if (teamRepository.count() > 0) {
            log.info("데이터가 이미 존재하여 초기 시드 데이터 생성을 건너뜁니다.");
            return;
        }

        log.info("=== PUBG eSports 초기 시드 데이터(선수/팀/대회/스탯) 주입 시작 ===");

        // 1. Teams 생성
        Team kdf = Team.builder().name("KWANGDONG FREECS").region("KR").logoUrl("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Kwangdong_Freecs_logo.svg/200px-Kwangdong_Freecs_logo.svg.png").build();
        Team geng = Team.builder().name("Gen.G").region("KR").logoUrl("https://upload.wikimedia.org/wikipedia/en/thumb/9/91/Gen.G_logo.svg/200px-Gen.G_logo.svg.png").build();
        Team danawa = Team.builder().name("Danawa e-sports").region("KR").logoUrl("https://i.namu.wiki/i/7u4mC-7x68uG8X.png").build();
        Team soniqs = Team.builder().name("Soniqs").region("AMER").logoUrl("https://i.namu.wiki/i/Soniqs_Logo.png").build();
        Team tm = Team.builder().name("Twisted Minds").region("EMEA").logoUrl("https://i.namu.wiki/i/Twisted_Minds.png").build();
        Team gaming17 = Team.builder().name("17Gaming").region("APAC").logoUrl("https://i.namu.wiki/i/17Gaming.png").build();
        Team cerberus = Team.builder().name("CERBERUS Esports").region("APAC").logoUrl("https://i.namu.wiki/i/Cerberus_Esports.png").build();
        Team navi = Team.builder().name("Natus Vincere").region("EMEA").logoUrl("https://i.namu.wiki/i/NAVI_logo.png").build();

        teamRepository.saveAll(List.of(kdf, geng, danawa, soniqs, tm, gaming17, cerberus, navi));

        // 2. Players & Settings & Gears
        // 2-1. Seoul (조기열)
        Player seoul = Player.builder()
                .team(danawa)
                .nickname("Seoul")
                .realName("조기열 (Gi-yeol Cho)")
                .role("IGL / Main Attacker")
                .country("KR")
                .profileImageUrl("https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=400&q=80")
                .youtubeUrl("https://www.youtube.com/@seoul_pubg")
                .chzzkUrl("https://chzzk.naver.com/")
                .soopUrl("https://bj.afreecatv.com/seoul")
                .isActive(true)
                .build();
        setPlayerTimestamp(seoul);

        PlayerSetting seoulSetting = PlayerSetting.builder()
                .player(seoul)
                .mouseDpi(800)
                .generalSens(28.0)
                .aimingSens(28.0)
                .adsSens(28.0)
                .scope2xSens(28.0)
                .scope3xSens(28.0)
                .scope4xSens(28.0)
                .scope6xSens(28.0)
                .verticalMultiplier(1.2)
                .fov(90)
                .resolution("1728x1080 (16:10)")
                .screenMode("전체 화면")
                .renderScale(100)
                .build();
        seoul.setSetting(seoulSetting);

        seoul.addGear(PlayerGear.builder().player(seoul).category("MOUSE").name("Logitech G PRO X SUPERLIGHT 2").brand("Logitech").build());
        seoul.addGear(PlayerGear.builder().player(seoul).category("MOUSEPAD").name("Artisan Ninja FX Zero Soft").brand("Artisan").build());
        seoul.addGear(PlayerGear.builder().player(seoul).category("KEYBOARD").name("Wooting 60HE").brand("Wooting").build());
        seoul.addGear(PlayerGear.builder().player(seoul).category("HEADSET").name("Sennheiser IE 200").brand("Sennheiser").build());
        seoul.addGear(PlayerGear.builder().player(seoul).category("MONITOR").name("BenQ ZOWIE XL2566K (360Hz)").brand("BenQ").build());

        seoul.addHighlight(PlayerHighlight.builder().player(seoul).title("PGC 2023 결승전 슈퍼플레이 매드무비").videoUrl("https://www.youtube.com/embed/dQw4w9WgXcQ").tournament("PGC 2023").build());

        // 2-2. Salute (우제현)
        Player salute = Player.builder()
                .team(kdf)
                .nickname("Salute")
                .realName("우제현 (Je-hyeon Woo)")
                .role("Main Attacker")
                .country("KR")
                .profileImageUrl("https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80")
                .youtubeUrl("https://www.youtube.com/")
                .chzzkUrl("https://chzzk.naver.com/")
                .isActive(true)
                .build();
        setPlayerTimestamp(salute);

        PlayerSetting saluteSetting = PlayerSetting.builder()
                .player(salute)
                .mouseDpi(800)
                .generalSens(33.0)
                .aimingSens(33.0)
                .adsSens(33.0)
                .verticalMultiplier(1.0)
                .fov(103)
                .resolution("1920x1080 (16:9)")
                .screenMode("전체 화면")
                .renderScale(100)
                .build();
        salute.setSetting(saluteSetting);
        salute.addGear(PlayerGear.builder().player(salute).category("MOUSE").name("Razer DeathAdder V3 Pro").brand("Razer").build());
        salute.addGear(PlayerGear.builder().player(salute).category("MOUSEPAD").name("SteelSeries QcK Heavy").brand("SteelSeries").build());
        salute.addGear(PlayerGear.builder().player(salute).category("KEYBOARD").name("Logitech G PRO X Keyboard").brand("Logitech").build());

        // 2-3. Inonix (나희주)
        Player inonix = Player.builder()
                .team(geng)
                .nickname("Inonix")
                .realName("나희주 (Hee-joo Na)")
                .role("All-Rounder / Attacker")
                .country("KR")
                .profileImageUrl("https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80")
                .isActive(true)
                .build();
        setPlayerTimestamp(inonix);

        PlayerSetting inonixSetting = PlayerSetting.builder()
                .player(inonix)
                .mouseDpi(400)
                .generalSens(50.0)
                .aimingSens(50.0)
                .adsSens(48.0)
                .verticalMultiplier(1.1)
                .fov(95)
                .resolution("1920x1080 (16:9)")
                .screenMode("전체 화면")
                .renderScale(100)
                .build();
        inonix.setSetting(inonixSetting);
        inonix.addGear(PlayerGear.builder().player(inonix).category("MOUSE").name("Zowie EC2-CW").brand("ZOWIE").build());
        inonix.addGear(PlayerGear.builder().player(inonix).category("MOUSEPAD").name("Zowie G-SR-SE Bi").brand("ZOWIE").build());

        // 2-4. Heaven (김태성)
        Player heaven = Player.builder()
                .team(kdf)
                .nickname("Heaven")
                .realName("김태성 (Tae-sung Kim)")
                .role("Main Attacker")
                .country("KR")
                .profileImageUrl("https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80")
                .isActive(true)
                .build();
        setPlayerTimestamp(heaven);

        PlayerSetting heavenSetting = PlayerSetting.builder()
                .player(heaven)
                .mouseDpi(800)
                .generalSens(30.0)
                .aimingSens(30.0)
                .adsSens(30.0)
                .verticalMultiplier(1.0)
                .fov(90)
                .resolution("1728x1080")
                .screenMode("전체 화면")
                .renderScale(100)
                .build();
        heaven.setSetting(heavenSetting);
        heaven.addGear(PlayerGear.builder().player(heaven).category("MOUSE").name("Logitech G PRO X SUPERLIGHT 2").brand("Logitech").build());

        // 2-5. TGLTN (James Giezen)
        Player tgltn = Player.builder()
                .team(soniqs)
                .nickname("TGLTN")
                .realName("James Giezen")
                .role("Fragger")
                .country("AU")
                .profileImageUrl("https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=400&q=80")
                .youtubeUrl("https://www.youtube.com/@TGLTN")
                .isActive(true)
                .build();
        setPlayerTimestamp(tgltn);

        PlayerSetting tgltnSetting = PlayerSetting.builder()
                .player(tgltn)
                .mouseDpi(800)
                .generalSens(24.0)
                .aimingSens(24.0)
                .adsSens(24.0)
                .verticalMultiplier(1.0)
                .fov(90)
                .resolution("1920x1080")
                .screenMode("전체 화면")
                .renderScale(100)
                .build();
        tgltn.setSetting(tgltnSetting);
        tgltn.addGear(PlayerGear.builder().player(tgltn).category("MOUSE").name("Logitech G PRO X SUPERLIGHT").brand("Logitech").build());

        playerRepository.saveAll(List.of(seoul, salute, inonix, heaven, tgltn));

        // 3. Tournaments & Twire.gg Style Leaderboards & Stats
        Tournament pgs4 = Tournament.builder()
                .name("PUBG Global Series 4 (PGS 4)")
                .slug("pgs-4-2024")
                .tier("S-Tier")
                .region("GLOBAL")
                .startDate(LocalDate.of(2024, 6, 3))
                .endDate(LocalDate.of(2024, 6, 9))
                .prizePool("$300,000")
                .location("Shanghai, China")
                .logoUrl("https://esports.pubg.com/assets/images/pgs4-logo.png")
                .status(Tournament.TournamentStatus.COMPLETED)
                .build();
        tournamentRepository.save(pgs4);

        // PGS 4 Team Leaderboard (Twire style)
        TournamentTeamResult r1 = TournamentTeamResult.builder().tournament(pgs4).team(tm).rank(1).totalPoints(152).killPoints(94).placementPoints(58).wwcdCount(3).matchesPlayed(18).prize("$100,000").build();
        TournamentTeamResult r2 = TournamentTeamResult.builder().tournament(pgs4).team(kdf).rank(2).totalPoints(141).killPoints(86).placementPoints(55).wwcdCount(2).matchesPlayed(18).prize("$40,000").build();
        TournamentTeamResult r3 = TournamentTeamResult.builder().tournament(pgs4).team(soniqs).rank(3).totalPoints(133).killPoints(81).placementPoints(52).wwcdCount(2).matchesPlayed(18).prize("$25,000").build();
        TournamentTeamResult r4 = TournamentTeamResult.builder().tournament(pgs4).team(danawa).rank(4).totalPoints(127).killPoints(78).placementPoints(49).wwcdCount(1).matchesPlayed(18).prize("$18,000").build();
        TournamentTeamResult r5 = TournamentTeamResult.builder().tournament(pgs4).team(cerberus).rank(5).totalPoints(119).killPoints(73).placementPoints(46).wwcdCount(1).matchesPlayed(18).prize("$15,000").build();
        TournamentTeamResult r6 = TournamentTeamResult.builder().tournament(pgs4).team(geng).rank(6).totalPoints(108).killPoints(65).placementPoints(43).wwcdCount(1).matchesPlayed(18).prize("$12,000").build();
        TournamentTeamResult r7 = TournamentTeamResult.builder().tournament(pgs4).team(gaming17).rank(7).totalPoints(99).killPoints(60).placementPoints(39).wwcdCount(1).matchesPlayed(18).prize("$10,000").build();
        TournamentTeamResult r8 = TournamentTeamResult.builder().tournament(pgs4).team(navi).rank(8).totalPoints(92).killPoints(55).placementPoints(37).wwcdCount(0).matchesPlayed(18).prize("$8,000").build();

        teamResultRepository.saveAll(List.of(r1, r2, r3, r4, r5, r6, r7, r8));

        // PGS 4 Player Stats (Twire style Kill & Damage leaders)
        TournamentPlayerStat ps1 = TournamentPlayerStat.builder().tournament(pgs4).player(heaven).rank(1).kills(34).damage(6120.5).knocks(31).assists(15).headshotRate(24.5).survivalTimeAvg(1280.0).twireRating(1.38).build();
        TournamentPlayerStat ps2 = TournamentPlayerStat.builder().tournament(pgs4).player(tgltn).rank(2).kills(31).damage(5840.0).knocks(28).assists(12).headshotRate(28.2).survivalTimeAvg(1210.0).twireRating(1.32).build();
        TournamentPlayerStat ps3 = TournamentPlayerStat.builder().tournament(pgs4).player(seoul).rank(3).kills(29).damage(5410.2).knocks(26).assists(18).headshotRate(31.0).survivalTimeAvg(1190.0).twireRating(1.29).build();
        TournamentPlayerStat ps4 = TournamentPlayerStat.builder().tournament(pgs4).player(salute).rank(4).kills(27).damage(5100.0).knocks(24).assists(14).headshotRate(22.8).survivalTimeAvg(1240.0).twireRating(1.24).build();
        TournamentPlayerStat ps5 = TournamentPlayerStat.builder().tournament(pgs4).player(inonix).rank(5).kills(23).damage(4320.0).knocks(20).assists(11).headshotRate(26.4).survivalTimeAvg(1080.0).twireRating(1.15).build();

        playerStatRepository.saveAll(List.of(ps1, ps2, ps3, ps4, ps5));

        log.info("=== PUBG eSports 시드 데이터 주입 완료! (팀 8개, 선수 5명, PGS 4 리더보드 & 스탯 등록 완료) ===");
    }

    private void setPlayerTimestamp(Player player) {
        try {
            java.lang.reflect.Field field = Player.class.getDeclaredField("lastCrawledAt");
            field.setAccessible(true);
            field.set(player, LocalDateTime.now());
        } catch (Exception ignored) {}
    }
}
