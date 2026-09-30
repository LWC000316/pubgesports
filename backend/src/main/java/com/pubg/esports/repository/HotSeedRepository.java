package com.pubg.esports.repository;

import com.pubg.esports.domain.HotSeed;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface HotSeedRepository extends JpaRepository<HotSeed, Long> {

    List<HotSeed> findAllByOrderBySeedRankAsc();
}
