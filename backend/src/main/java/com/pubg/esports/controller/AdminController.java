package com.pubg.esports.controller;

import com.pubg.esports.dto.AdminPlayerRequestDto;
import com.pubg.esports.dto.AdminTeamRequestDto;
import com.pubg.esports.service.AdminService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final AdminService adminService;

    @PostMapping("/teams")
    public ResponseEntity<Map<String, Object>> createTeam(@RequestBody AdminTeamRequestDto dto) {
        Long teamId = adminService.createTeam(dto);
        return ResponseEntity.ok(Map.of("success", true, "id", teamId, "message", "팀이 성공적으로 등록되었습니다."));
    }

    @PutMapping("/teams/{id}")
    public ResponseEntity<Map<String, Object>> updateTeam(@PathVariable Long id, @RequestBody AdminTeamRequestDto dto) {
        adminService.updateTeam(id, dto);
        return ResponseEntity.ok(Map.of("success", true, "id", id, "message", "팀 정보가 성공적으로 수정되었습니다."));
    }

    @DeleteMapping("/teams/{id}")
    public ResponseEntity<Map<String, Object>> deleteTeam(@PathVariable Long id) {
        adminService.deleteTeam(id);
        return ResponseEntity.ok(Map.of("success", true, "message", "팀이 삭제되었습니다."));
    }

    @PostMapping("/players")
    public ResponseEntity<Map<String, Object>> createPlayer(@RequestBody AdminPlayerRequestDto dto) {
        Long playerId = adminService.createPlayer(dto);
        return ResponseEntity.ok(Map.of("success", true, "id", playerId, "message", "선수가 성공적으로 등록되었습니다."));
    }

    @PutMapping("/players/{id}")
    public ResponseEntity<Map<String, Object>> updatePlayer(@PathVariable Long id, @RequestBody AdminPlayerRequestDto dto) {
        adminService.updatePlayer(id, dto);
        return ResponseEntity.ok(Map.of("success", true, "id", id, "message", "선수 정보 및 세팅이 성공적으로 수정되었습니다."));
    }

    @DeleteMapping("/players/{id}")
    public ResponseEntity<Map<String, Object>> deletePlayer(@PathVariable Long id) {
        adminService.deletePlayer(id);
        return ResponseEntity.ok(Map.of("success", true, "message", "선수가 삭제되었습니다."));
    }
}
