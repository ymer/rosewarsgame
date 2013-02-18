//
//  Attribute.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "BaseRangedAttribute.h"
#import "RawBonus.h"
#import "TimedBonus.h"

typedef enum {
    
    kRangedAttributeLowerValue,
    kRangedAttributeUpperValue
} RangedAttributeValues;

@class RangeAttribute;
@protocol RangeAttributeDelegate <NSObject>

@optional

- (void)rangeAttribute:(RangeAttribute*)attribute addedRawBonus:(RawBonus*)rawBonus;
- (void)rangeAttribute:(RangeAttribute*)attribute addedTimedBonus:(TimedBonus*)timedBonus;

- (void)rangeAttribute:(RangeAttribute*)attribute removedRawBonus:(RawBonus*)rawBonus;
- (void)rangeAttribute:(RangeAttribute*)attribute removedTimedBonus:(TimedBonus*)timedBonus;

@end

@interface RangeAttribute : BaseRangedAttribute {
    
    NSMutableArray *_rawBonuses;
    NSMutableArray *_timedBonuses;
}

@property (nonatomic, weak) id<RangeAttributeDelegate> delegate;
@property (nonatomic, readonly) AttributeRange finalRange;
@property (nonatomic, assign) RangedAttributeValues valueAffectedByBonuses;

- (id)initWithStartingRange:(AttributeRange)startingRange;

- (void)addRawBonus:(RawBonus*)rawBonus;
- (NSUInteger)getRawBonusValue;

- (void)addTimedBonus:(TimedBonus*)timedBonus;
- (NSUInteger)getTimedBonusValue;

- (void)removeRawBonus:(RawBonus*)rawBonus;
- (void)removeTimedBonus:(TimedBonus*)timedBonus;

- (AttributeRange)calculateValue;

@end
