//
//  RandomDeckStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import "RandomDeckStrategy.h"
#import "CardPool.h"
#import "Deck.h"

@implementation RandomDeckStrategy

+ (id)strategy {
    
    return [[RandomDeckStrategy alloc] init];
}

- (NSArray*)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor {
    
    _cards = [[NSMutableArray alloc] init];
    
    CardPool *cardPool = [[CardPool alloc] init];
    
    NSInteger numberOfBasicTypes = 0;
    NSInteger numberOfSpecialTypes = 0;
    
    while (numberOfBasicTypes < basicType) {
        
        Card *drawnCard = [cardPool drawCardOfCardType:kCardTypeBasicUnit];
        
        drawnCard.cardColor = cardColor;
        
        if ([self cardIsAllowedInDeck:drawnCard]) {
            [_cards addObject:drawnCard];
            numberOfBasicTypes++;
        }
    }
    
    while (numberOfSpecialTypes < specialType) {
        
        Card *drawnCard = [cardPool drawCardOfCardType:kCardTypeSpecialUnit];
        
        drawnCard.cardColor = cardColor;
        
        if ([self cardIsAllowedInDeck:drawnCard]) {
            [_cards addObject:drawnCard];
            numberOfSpecialTypes++;
        }
    }
    
    return [NSArray arrayWithArray:_cards];
}

- (void)placeCardsInDeck:(Deck *)deck inGameBoardSide:(GameBoardSides)gameBoardSide {
    
    NSUInteger offset = 0;
    
    for (Card *card in deck.cards) {
        
        BOOL cardInValidPosition = NO;
        
        while (!cardInValidPosition) {
            
            GridLocation *location = [GridLocation gridLocationWithRow:(arc4random() % 4) + 1 + offset column:(arc4random() % 5) + 1];
            
            if (![self deck:deck containsCardInLocation:location]) {
                
                card.cardLocation = location;
                cardInValidPosition = YES;
            }
        }
    }
}


@end
