package com.pubg.esports.service;

import com.pubg.esports.domain.Tournament;
import com.pubg.esports.dto.PlayerStatDto;
import com.pubg.esports.dto.TeamResultDto;
import com.pubg.esports.dto.TournamentDetailDto;
import com.pubg.esports.dto.TournamentListDto;
import com.pubg.esports.repository.TournamentPlayerStatRepository;
import com.pubg.esports.repository.TournamentRepository;
import com.pubg.esports.repository.TournamentTeamResultRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TournamentService {

    private final TournamentRepository tournamentRepository;
    private final TournamentTeamResultRepository teamResultRepository;
    private final TournamentPlayerStatRepository playerStatRepository;

    public List<TournamentListDto> getAllTournaments() {
        return tournamentRepository.findAllOrderByStartDateDesc().stream()
                .map(TournamentListDto::from)
                .collect(Collectors.toList());
    }

    public TournamentDetailDto getTournamentDetail(Long tournamentId) {
        Tournament tournament = tournamentRepository.findById(tournamentId)
                .orElseThrow(() -> new IllegalArgumentException("대회를 찾을 수 없습니다. ID: " + tournamentId));
        return TournamentDetailDto.from(tournament);
    }

    public TournamentDetailDto getTournamentBySlug(String slug) {
        Tournament tournament = tournamentRepository.findBySlug(slug)
                .orElseThrow(() -> new IllegalArgumentException("대회를 찾을 수 없습니다. Slug: " + slug));
        return TournamentDetailDto.from(tournament);
    }

    public List<TeamResultDto> getTournamentLeaderboard(Long tournamentId) {
        return teamResultRepository.findByTournamentIdOrderByRankAsc(tournamentId).stream()
                .map(TeamResultDto::from)
                .collect(Collectors.toList());
    }

    public List<PlayerStatDto> getTournamentPlayerStats(Long tournamentId) {
        return playerStatRepository.findByTournamentIdOrderByKillsDesc(tournamentId).stream()
                .map(PlayerStatDto::from)
                .collect(Collectors.toList());
    }
}
