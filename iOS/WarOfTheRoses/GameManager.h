//
//  GameManager.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import <Foundation/Foundation.h>
#import "Game.h"
#import "AIPlayer.h"
#import "DiceStrategy.h"
#import "DeckStrategy.h"

@protocol GameManagerProtocol <NSObject>

- (void)turnChangedToPlayerWithColor:(PlayerColors)player;

- (void)combatHasStartedBetweenAttacker:(Card*)attacker andDefender:(Card*)defender;
- (void)cardHasBeenDefeatedInCombat:(Card*)card;

@end

@interface GameManager : NSObject {
    
    AIPlayer *_enemyPlayer;
    NSUInteger _turnCounter;
}

@property (nonatomic, weak) id<GameManagerProtocol> delegate;
@property (nonatomic, strong) Game *currentGame;
@property (nonatomic, assign) PlayerColors currentPlayersTurn;

@property (nonatomic, strong) id<DiceStrategy> attackerDiceStrategy;
@property (nonatomic, strong) id<DiceStrategy> defenderDiceStrategy;
@property (nonatomic, strong) id<DeckStrategy> deckStrategy;

- (Action*)getActionForEnemeyPlayer;
- (CombatOutcome)resolveCombatBetween:(Card*)attacker defender:(Card*)defender;

- (NSUInteger)actionUsed:(Action*)action;

- (void)startNewGameOfType:(GameTypes)gameType;
- (BOOL)shouldEndTurn;
- (void)endTurn;

- (void)card:(Card*)card movedToGridLocation:(GridLocation*)location;
- (void)cardHasBeenDefeated:(Card*)card;

- (GameResults)checkForEndGame;

+ (GameManager*)sharedManager;

@end