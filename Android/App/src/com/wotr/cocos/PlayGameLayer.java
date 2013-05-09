package com.wotr.cocos;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;

import org.cocos2d.actions.ease.CCEaseSineIn;
import org.cocos2d.actions.instant.CCCallback;
import org.cocos2d.actions.interval.CCDelayTime;
import org.cocos2d.actions.interval.CCFadeIn;
import org.cocos2d.actions.interval.CCFadeOut;
import org.cocos2d.actions.interval.CCMoveTo;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.actions.interval.CCTintTo;
import org.cocos2d.layers.CCLayer;
import org.cocos2d.layers.CCScene;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCLabel;
import org.cocos2d.nodes.CCNode;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.sound.SoundEngine;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;
import org.cocos2d.types.ccColor3B;

import android.content.res.AssetFileDescriptor;
import android.media.MediaPlayer;
import android.view.MotionEvent;

import com.wotr.GameManager;
import com.wotr.R;
import com.wotr.cocos.action.RemoveNodeCallBackAction;
import com.wotr.cocos.nodes.ActionPathSprite;
import com.wotr.cocos.nodes.BonusChooserSprite;
import com.wotr.cocos.nodes.CardSprite;
import com.wotr.cocos.nodes.GoSprite;
import com.wotr.model.Action;
import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.action.ActionCollection;
import com.wotr.strategy.action.ActionsResolver;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.action.PathFinderStrategy;
import com.wotr.strategy.action.ShortestPathFinderStrategy;
import com.wotr.strategy.battle.BattleListener;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.GameEventListener;
import com.wotr.strategy.game.MultiplayerGame;
import com.wotr.strategy.game.exceptions.InvalidActionException;
import com.wotr.strategy.game.exceptions.InvalidAttackException;
import com.wotr.strategy.game.exceptions.InvalidEndPositionException;
import com.wotr.strategy.game.exceptions.InvalidMoveException;
import com.wotr.strategy.player.HumanPlayer;
import com.wotr.strategy.player.Player;
import com.wotr.touch.CardTouchHandler;
import com.wotr.touch.CardTouchListener;

public class PlayGameLayer extends AbstractGameLayer implements CardTouchListener, GameEventListener, BattleListener {

	private Collection<CardSprite> unitList = new ArrayList<CardSprite>();
	private int xCount;
	private int yCount;
	private ActionCollection<Action> actionCollection;
	private CCLabel nameLabel;
	private CCLabel turnLabel;
	private Player playerOne;
	private ActionsResolverStrategy actionsResolver;

	private PathFinderStrategy pathFinderStrategy;
	private ActionPathSprite actionPathSprite;
	private AttackResult attackResult;

	public static CCScene scene(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap) {
		CCScene scene = CCScene.node();
		CCLayer layer = new PlayGameLayer(playerOneMap, playerTwoMap);
		scene.addChild(layer);
		return scene;
	}

	protected PlayGameLayer(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap) {

		xCount = 5;
		yCount = 8;

		playerOne = new HumanPlayer(playerOneMap, "Player 1", 0);
		Player playerTwo = new HumanPlayer(playerTwoMap, "Player 2", yCount - 1);

		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		CCSprite back = new CCSprite("woddenbackground.png");

		back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		addChild(back);

		CCSprite prototype = new CCSprite("unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		tch = new CardTouchHandler();
		tch.addListener(this);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;

		addBackGroundCards(xCount, yCount, true);
		addCards(playerOneMap);
		addCards(playerTwoMap);

		nameLabel = CCLabel.makeLabel("    ", "Arial", 60f);
		nameLabel.setPosition(10f, winSize.getHeight() - 80f);
		nameLabel.setAnchorPoint(0, 0);
		nameLabel.setColor(ccColor3B.ccWHITE);
		nameLabel.setOpacity(200);
		addChild(nameLabel, 10);

		turnLabel = CCLabel.makeLabel("    ", "Arial", 60f);
		turnLabel.setPosition(winSize.getWidth() - 50f, winSize.getHeight() - 80f);
		turnLabel.setAnchorPoint(0, 0);
		turnLabel.setColor(ccColor3B.ccWHITE);
		turnLabel.setOpacity(200);
		addChild(turnLabel, 10);

		Game game = new MultiplayerGame(playerOne, playerTwo);
		game.addGameEventListener(this);
		GameManager.setGame(game);
		GameManager.getFactory().getBattleStrategy().addBattleListener(this);

		actionsResolver = new ActionsResolver(xCount, yCount, game);
		game.setActionsResolver(actionsResolver);

		game.startGame();
		
		
		BonusChooserSprite bcs = new BonusChooserSprite();
		bcs.setPosition(CGPoint.ccp(winSize.getWidth() / 2f, winSize.getHeight() / 2f));
		addChild(bcs);
	}

	protected void dropCardToPosition() {
		CCScaleTo scaleAction = CCScaleTo.action(0.3f, sizeScale);
		selectedCard.runAction(scaleAction);
	}

	private void addCards(UnitMap<Position, Unit> playerCards) {

		for (Unit card : playerCards.values()) {
			CardSprite cardSprite = new CardSprite(card, sizeScale, bordframe);
			addChild(cardSprite);
			unitList.add(cardSprite);

			cardSprite.drawBonus();
		}
	}

	@Override
	public void cardDragedEnded(float x, float y) {

		resetActionSelection();

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			moveCardToOriginalPosition();
			removeSelection();
		} else {

			Unit attackingUnit = (Unit) selectedCard.getUserData();

			// If player has card at position
			if (GameManager.getGame().getAttackingPlayer().hasUnitAtPosition(pInP)) {
				moveCardToOriginalPosition();
				removeSelection();
			} else {

				Unit defendingUnit = GameManager.getGame().getDefendingPlayer().getUnitAtPosition(pInP);
				pathFinderStrategy.getActionForPosition(pInP);

				try {
					// if defending unit found on position, perform attack
					if (defendingUnit != null) {
						cardDragedEndedOnDefendingUnit(attackingUnit, defendingUnit, pInP);
					} else {
						cardDragedEndedOnEmptyPosition(attackingUnit, pInP);
						removeSelection();
					}
				} catch (InvalidActionException e) {
					moveCardToOriginalPosition();
				}
			}
		}
	}

	private void removeSelection() {
		reorderChild(selectedCard, 1);
		selectedCard = null;
	}

	private void cardDragedEndedOnEmptyPosition(Unit attackingUnit, Position pInP) throws InvalidMoveException {

		dropCardToPosition();

		GameManager.getGame().move(attackingUnit, pInP);
		SoundEngine.sharedEngine().playEffect(CCDirector.sharedDirector().getActivity(), R.raw.pageflip);
	}

	private void cardDragedEndedOnDefendingUnit(Unit attackingUnit, Unit defendingUnit, Position pInP) throws InvalidEndPositionException, InvalidAttackException {

		Action action = pathFinderStrategy.getActionForPosition(pInP);
		attackResult = GameManager.getGame().attack(action, defendingUnit);

		if (attackResult.isSuccesfull()) {
			removeCCSprite(defendingUnit);
		}

		List<Position> endPositions = attackResult.getEndPositions();
		if (endPositions.size() == 1) {
			attackResult = null;
			moveCardToPosition(endPositions.get(0));
			removeSelection();
		} else {

			dropCardToPosition();

			// Add images to selection en positions for
			for (Position endPosition : endPositions) {
				GoSprite goSprite = new GoSprite(endPosition, sizeScale, bordframe);
				addChild(goSprite, 10);
			}
		}
	}

	private void resetActionSelection() {

		removePathSprite();

		Collection<Position> attackPositions = actionCollection.getAttackPositions();
		for (Position position : attackPositions) {
			for (CCNode ccNode : unitList) {

				Unit unit = (Unit) ccNode.getUserData();
				if (position.equals(unit.getPosition())) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccWHITE);
					ccNode.runAction(tin);
				}
			}
		}

		Collection<Position> movePositions = actionCollection.getMovePositions();
		for (Position position : movePositions) {
			for (CCNode ccNode : cardBackgroundList) {
				Position pos = (Position) ccNode.getUserData();
				if (position.equals(pos)) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccWHITE);
					ccNode.runAction(tin);
				}
			}
		}

		selectedCard.setOpacity(255);
	}

	protected void selectCardForMove(CCSprite selectedCard) {
		super.selectCardForMove(selectedCard);

		Unit unit = (Unit) selectedCard.getUserData();

		actionCollection = actionsResolver.getActions(unit);
		pathFinderStrategy = new ShortestPathFinderStrategy(actionCollection);

		for (Position position : actionCollection.getAttackPositions()) {
			for (CCNode ccNode : unitList) {
				Unit u = (Unit) ccNode.getUserData();
				if (position.equals(u.getPosition())) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccRED);
					ccNode.runAction(tin);
				}
			}
		}

		for (Position position : actionCollection.getMovePositions()) {
			for (CCNode ccNode : cardBackgroundList) {
				Position pos = (Position) ccNode.getUserData();
				if (position.equals(pos)) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccGREEN);
					ccNode.runAction(tin);
				}
			}
		}
	}

	@Override
	public void cardMoved(float x, float y) {
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			selectedCard.setPosition(x, y);
		} else {
			CGPoint position = bordframe.getPosition(pInP.getX(), pInP.getY());

			if (!CGPoint.equalToPoint(selectedCard.getPosition(), position)) {
				selectedCard.setPosition(position);
				pathFinderStrategy.touch(pInP);
				Action action = pathFinderStrategy.getActionForPosition(pInP);

				removePathSprite();

				if (action != null) {
					actionPathSprite = new ActionPathSprite(action, bordframe);
					addChild(actionPathSprite);
				}
			}
		}
	}

	private void removePathSprite() {
		if (actionPathSprite != null) {
			removeChild(actionPathSprite, true);
		}
	}

	@Override
	public void cardSelected(float x, float y) {
		moveCardToCenterAndEnlarge();
	}

	@Override
	public void cardDeSelected(float x, float y) {
		resetActionSelection();
		moveCardToOriginalPosition();
	}

	@Override
	protected Collection<CardSprite> getCardSprites() {
		return unitList;
	}

	@Override
	public void gameStarted() {
	}

	@Override
	public void startTurn(Player player, int actionsLeft) {
		turnLabel.setString("" + actionsLeft);
		nameLabel.setString(player.getName());

		if (player.equals(playerOne)) {
			turnLabel.setColor(ccColor3B.ccGREEN);
			nameLabel.setColor(ccColor3B.ccGREEN);
		} else {
			turnLabel.setColor(ccColor3B.ccRED);
			nameLabel.setColor(ccColor3B.ccRED);
		}
	}

	@Override
	public void actionPerformed(Player player, int remainingActions) {
		startTurn(player, remainingActions);
	}

	@Override
	protected boolean isTurn(Unit unit) {
		return GameManager.getGame().getAttackingPlayer().hasUnit(unit);
	}

	private void removeCCSprite(Unit defendingUnit) {

		for (Iterator<CardSprite> i = unitList.iterator(); i.hasNext();) {
			CCSprite unitSpite = i.next();
			Unit unit = (Unit) unitSpite.getUserData();
			if (unit.equals(defendingUnit)) {
				i.remove();
				removeChild(unitSpite, true);
				return;
			}
		}
	}

	@Override
	public void attackStarted(Unit attacker, Unit defender) {

		MediaPlayer mp = new MediaPlayer();
		try {
			AssetFileDescriptor afd = CCDirector.sharedDirector().getActivity().getAssets().openFd(attacker.getAttackSound());
			mp.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
			mp.prepare();
			mp.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void attackSuccessful(Unit attacker, Unit defender, int attackRoll) {

		CCLabel actionLabel = CCLabel.makeLabel("Attack succesful (" + attackRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);

		addChild(actionLabel);

		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(moveAction, fadeAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));

	}

	@Override
	public void attackFailed(Unit attacker, Unit defender, int attackRoll) {

		// CCNode node = CCNode.node();
		// node.setPosition(winSize.width / 2, winSize.height - winSize.height /
		// 3f);

		// CCSprite dice = CCSprite.sprite("dice/1.png");
		// dice.setPosition(100f, 10f);
		// node.addChild(dice);

		CCLabel actionLabel = CCLabel.makeLabel("Missed (" + attackRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		// node.addChild(actionLabel);

		addChild(actionLabel);

		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(moveAction, fadeAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));
	}

	@Override
	public void defenceStarted(Unit attacker, Unit defender) {

	}

	@Override
	public void defenceSuccessful(Unit attacker, Unit defender, int defenceRoll) {
		CCLabel actionLabel = CCLabel.makeLabel("Defence succesful (" + defenceRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		actionLabel.setOpacity(0);

		addChild(actionLabel);

		CCDelayTime delayAction = CCDelayTime.action(0.1f);
		CCFadeIn fadeInAction = CCFadeIn.action(0.3f);
		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(delayAction, fadeInAction, moveAction, fadeAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));
	}

	@Override
	public void defenceFailed(Unit attacker, Unit defender, int defenceRoll) {

		MediaPlayer mp = new MediaPlayer();
		try {
			AssetFileDescriptor afd = CCDirector.sharedDirector().getActivity().getAssets().openFd(defender.getKilledSound());
			mp.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
			mp.prepare();
			mp.start();
		} catch (Exception e) {
			e.printStackTrace();
		}

		CCLabel actionLabel = CCLabel.makeLabel("Defence failed (" + defenceRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		actionLabel.setOpacity(0);

		addChild(actionLabel);

		CCDelayTime delayAction = CCDelayTime.action(0.1f);
		CCFadeIn fadeInAction = CCFadeIn.action(0.3f);
		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeOutAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(delayAction, fadeInAction, moveAction, fadeOutAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));
	}

	@Override
	public void gameEnded(Player winner) {

		CCLabel winnerLabel = CCLabel.makeLabel("Winner: " + winner.getName(), "Arial", 40f);
		winnerLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		addChild(winnerLabel);

		MediaPlayer mp = new MediaPlayer();
		try {
			AssetFileDescriptor afd = CCDirector.sharedDirector().getActivity().getAssets().openFd("sounds/fanfare.mp3");
			mp.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
			mp.prepare();
			mp.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public boolean ccTouchesBegan(MotionEvent event) {

		// if waiting for input about where to end successful attack
		if (attackResult != null) {
			endAttack(event);
			
			
			attackResult = null;
			removeSelection();
			return true;

		} else {
			return super.ccTouchesBegan(event);
		}
	}

	private void endAttack(MotionEvent event) {

		Collection<GoSprite> goSprites = new ArrayList<GoSprite>();

		List<CCNode> children = getChildren();
		for (CCNode ccNode : children) {
			if (ccNode instanceof GoSprite) {
				GoSprite go = (GoSprite) ccNode;
				goSprites.add(go);
				if (ccNode.getBoundingBox().contains(event.getRawX(), winSize.height - event.getRawY())) {

					Position position = go.getPositionUserData();
					try {
						attackResult.endAttackAt(position);
					} catch (InvalidEndPositionException e) {
						e.printStackTrace();
					}
					moveCardToPosition(position);
				}
			}
		}

		for (GoSprite goSprite : goSprites) {
			removeChild(goSprite, true);
		}		
	}
}
