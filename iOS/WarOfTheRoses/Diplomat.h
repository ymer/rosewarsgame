//
//  Diplomat.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/20/13.
//
//

#import "Card.h"

@interface Diplomat : Card {
    
    Card *_bribedOpponent;
    NSUInteger _opponentBribedInRound;
}

+ (id)card;

@end
