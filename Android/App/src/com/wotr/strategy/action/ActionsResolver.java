package com.wotr.strategy.action;

import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.wotr.GameManager;
import com.wotr.model.Action;
import com.wotr.model.ActionPath;
import com.wotr.model.ActionPathLink;
import com.wotr.model.AttackAction;
import com.wotr.model.Direction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.GameEventListener;
import com.wotr.strategy.game.TurnStrategy;
import com.wotr.strategy.player.Player;

public class ActionsResolver implements ActionsResolverStrategy, GameEventListener {

	private final int yRange;
	private final int xRange;
	private final Game game;

	private Map<Unit, Collection<Action>> actionCache = new HashMap<Unit, Collection<Action>>();

	public ActionsResolver(int xRange, int yRange, Game game) {
		this.yRange = yRange;
		this.xRange = xRange;
		this.game = game;

		// Add action resolver as game event listener to clear action cache
		// after turn
		game.addGameEventListener(this);
	}

	public Collection<Action> getActions(Unit originalunit) {

		Collection<Action> actions = actionCache.get(originalunit);
		if (actions == null) {
			TurnStrategy turnStrategy = GameManager.getFactory().getTurnStrategy();
			Map<Position, Unit> aUnits = game.getAttackingPlayer().getUnitMap();
			Map<Position, Unit> dUnits = game.getDefendingPlayer().getUnitMap();

			UnitActionResolverStrategy actionResolverStrategy = originalunit.getActionResolverStrategy();
			actions = getActions(originalunit, originalunit.getPosition(), null, true, aUnits, dUnits, 0, actionResolverStrategy, turnStrategy);
			actionCache.put(originalunit, actions);
		}
		return actions;
	}

	private Set<Action> getActions(Unit originalUnit, Position pos, ActionPath path, boolean moveable, Map<Position, Unit> aUnits, Map<Position, Unit> dUnits, int pathProgress, UnitActionResolverStrategy ars, TurnStrategy turnStrategy) {

		Set<Action> moves = new HashSet<Action>();

		int pathLength = ars.getPathLength(originalUnit, pos, path, aUnits, dUnits, pathProgress);
		if (pathProgress < pathLength + 1) {

			if (!originalUnit.getPosition().equals(pos)) {

				if (ars.isAttackable(originalUnit, pos, path, aUnits, dUnits, pathProgress, turnStrategy)) {
					moves.add(new AttackAction(originalUnit, pos, path));
				} else if (moveable = ars.isMoveable(originalUnit, pos, path, moveable, aUnits, dUnits, pathProgress, turnStrategy)) {
					moves.add(new MoveAction(originalUnit, pos, path));
				}
			}

			Collection<Direction> directions = ars.getDirections(originalUnit, pos, path, aUnits, dUnits, pathProgress);
			for (Direction direction : directions) {
				Position movePosition = pos.move(direction);
				if (isInBoard(movePosition)) {					
					ActionPath link = new ActionPathLink(movePosition, path);
					moves.addAll(getActions(originalUnit, movePosition, link, moveable, aUnits, dUnits, pathProgress + 1, ars, turnStrategy));
				}
			}
		}

		return moves;
	}

	private boolean isInBoard(Position movedPosition) {
		return movedPosition.getX() >= 0 && movedPosition.getY() >= 0 && movedPosition.getX() < xRange && movedPosition.getY() < yRange;
	}

	@Override
	public void gameStarted() {
		actionCache.clear();
	}

	@Override
	public void startTurn(Player player, int remainingActions) {
		actionCache.clear();
	}

	@Override
	public void actionPerformed(Player player, int remainingActions) {
		actionCache.clear();
	}

	@Override
	public void gameEnded(Player winner) {
		actionCache.clear();
	}
}
