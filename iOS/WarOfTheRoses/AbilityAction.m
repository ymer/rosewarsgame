//
//  AbilityAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "AbilityAction.h"
#import "AbilityFactory.h"

@implementation AbilityAction

@synthesize actionType = _actionType;
@synthesize startLocation = _startLocation;
@synthesize availableAbilities = _availableAbilities;
@synthesize battleReport = _battleReport;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card targetCard:(Card *)targetCard {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:targetCard];
    
    if (self) {
        _actionType = kActionTypeAbility;
        _startLocation = card.cardLocation;
        
        _availableAbilities = [NSArray arrayWithArray:self.cardInAction.abilities];
    }
    
    return self;
}

- (BOOL)isAttack {
    
    return NO;
}

- (NSUInteger)cost {
    
    return 1;
}

- (ActionTypes)actionType {
    
    return kActionTypeAbility;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    _battleReport = [BattleReport battleReportWithAction:self];

    [[GameManager sharedManager] willUseAction:self];
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    if (_availableAbilities.count == 1) {
        _abilityUsed = [AbilityFactory addAbilityOfType:(AbilityTypes)[_availableAbilities[0] integerValue] onCard:self.enemyCard];
    }
        
    [[GameManager sharedManager] actionUsed:self];
    [self.cardInAction didPerformedAction:self];
    
    [[GameManager sharedManager].currentGame addBattleReport:_battleReport forAction:self];
    
    [self.delegate afterPerformAction:self];
    
    if (completion != nil) {
        completion();
    }
}
@end