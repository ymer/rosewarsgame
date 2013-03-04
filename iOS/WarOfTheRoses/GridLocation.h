//
//  Position.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import <Foundation/Foundation.h>

@interface GridLocation : NSObject <NSCopying>

@property (nonatomic, assign) NSUInteger row;
@property (nonatomic, assign) NSUInteger column;

+ (id)gridLocationWithRow:(NSUInteger)row column:(NSUInteger)column;
- (id)initWithRow:(NSUInteger)row column:(NSUInteger)column;

- (NSArray*)perpendicularGridLocations;
- (NSArray*)surroundingGridLocations;

- (GridLocation*)locationAbove;
- (GridLocation*)locationBelow;
- (GridLocation*)locationToTheLeft;
- (GridLocation*)locationToTheRight;

@end