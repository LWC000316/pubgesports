package com.pubg.esports.service;

import com.pubg.esports.domain.Player;
import com.pubg.esports.domain.Team;
import com.pubg.esports.dto.PlayerDetailResponseDto;
import com.pubg.esports.dto.PlayerListResponseDto;
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
        List<Player> players = playerRepository.searchPlayers(teamId, query);
        return players.stream()
                .map(PlayerListResponseDto::from)
                .collect(Collectors.toList());
    }

    public PlayerDetailResponseDto getPlayerDetail(Long playerId) {
        Player player = playerRepository.findById(playerId)
                .orElseThrow(() -> new IllegalArgumentException("선수를 찾을 수 없습니다. ID: " + playerId));
        return PlayerDetailResponseDto.from(player);
    }

    public PlayerDetailResponseDto getPlayerByNickname(String nickname) {
        Player player = playerRepository.findByNicknameIgnoreCase(nickname)
                .orElseThrow(() -> new IllegalArgumentException("선수를 찾을 수 없습니다. Nickname: " + nickname));
        return PlayerDetailResponseDto.from(player);
    }

    public List<TeamResponseDto> getAllTeams() {
        return teamRepository.findAll().stream()
                .map(TeamResponseDto::from)
                .collect(Collectors.toList());
    }
}
