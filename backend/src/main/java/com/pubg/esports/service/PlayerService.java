package com.pubg.esports.service;

import com.pubg.esports.domain.Player;
import com.pubg.esports.domain.Team;
import com.pubg.esports.dto.PlayerDetailResponseDto;
import com.pubg.esports.dto.PlayerListResponseDto;
import com.pubg.esports.dto.TeamCardDto;
import com.pubg.esports.dto.TeamResponseDto;
import com.pubg.esports.repository.PlayerRepository;
import com.pubg.esports.repository.TeamRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class PlayerService {

    private final PlayerRepository playerRepository;
    private final TeamRepository teamRepository;

    public List<PlayerListResponseDto> getPlayers(Long teamId, String query) {
        boolean hasTeam = teamId != null;
        boolean hasQuery = query != null && !query.trim().isEmpty();
        List<Player> players;

        if (hasTeam && hasQuery) {
            players = playerRepository.searchByTeamIdAndQueryWithTeam(teamId, query.trim());
        } else if (hasTeam) {
            players = playerRepository.findByTeamIdWithTeam(teamId);
        } else if (hasQuery) {
            players = playerRepository.searchByQueryWithTeam(query.trim());
        } else {
            players = playerRepository.findAllWithTeam();
        }

        return players.stream()
                .map(PlayerListResponseDto::from)
                .collect(Collectors.toList());
    }

    /** 없는 선수면 {@code null}. 컨트롤러가 404 로 바꾼다. */
    public PlayerDetailResponseDto getPlayerDetail(Long playerId) {
        return playerRepository.findById(playerId)
                .map(PlayerDetailResponseDto::from)
                .orElse(null);
    }

    public PlayerDetailResponseDto getPlayerByNickname(String nickname) {
        return playerRepository.findByNicknameIgnoreCase(nickname)
                .map(PlayerDetailResponseDto::from)
                .orElse(null);
    }

    public List<TeamResponseDto> getAllTeams() {
        return teamRepository.findAll().stream()
                .map(TeamResponseDto::from)
                .collect(Collectors.toList());
    }

    public List<TeamCardDto> getTeamCards(String league) {
        return teamRepository.findByLeagueWithPlayers(league).stream()
                .map(TeamCardDto::from)
                .collect(Collectors.toList());
    }
}
