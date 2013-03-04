package com.wotr.strategy.action;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.facade.ActionResolverFactory;

public class MeleeActionResolverStrategy extends AbstractActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, Direction direction, boolean movable, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return super.isMoveable(unit, pos, direction, movable, attackingUnits, defendingUnits, pathProgress) && pathProgress <= unit.getMovement();
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return super.isAttackable(unit, pos, direction, attackingUnits, defendingUnits, pathProgress) && pathProgress <= unit.getMovement();
	}

	@Override
	public Collection<Direction> getDirections(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {

		// If pos has any unit, Melee units will not be able to move or attack any further
		if (!unit.getPosistion().equals(pos) && (attackingUnits.containsKey(pos) || defendingUnits.containsKey(pos))) {
			return Collections.emptyList();
		} else {
			return getZocDirections(unit, pos, direction, attackingUnits, defendingUnits, pathProgress);
		}
	}

	private Collection<Direction> getZocDirections(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		List<Direction> result = new ArrayList<Direction>();
		ZocBlockStrategy zbs = ActionResolverFactory.getZocBlockStrategy();

		for (Direction d : Direction.perpendicularDirections) {
			if (!zbs.isDirectionBlocked(unit, d, pos, attackingUnits, defendingUnits)) {
				result.add(d);
				result.add(d.opposite());
			}
		}
		return result;
	}
}