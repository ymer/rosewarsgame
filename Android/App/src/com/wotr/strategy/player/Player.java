package com.wotr.strategy.player;

import java.util.Map;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public interface Player {

	String getName();

	Map<Position, Unit> getUnitMap();

}
