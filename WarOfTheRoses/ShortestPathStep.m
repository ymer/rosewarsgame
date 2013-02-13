//
//  ShortestPathStep.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import "ShortestPathStep.h"

@implementation ShortestPathStep

@synthesize location;
@synthesize gScore;
@synthesize hScore;
@synthesize parent;

- (id)initWithLocation:(GridLocation)loc
{
	if ((self = [super init])) {
		location = loc;
		gScore = 0;
		hScore = 0;
		parent = nil;
	}
    
	return self;
}

- (NSString *)description
{
	return [NSString stringWithFormat:@"%@  pos=[%d;%d]  g=%d  h=%d  f=%d", [super description], self.location.column, self.location.row, self.gScore, self.hScore, [self fScore]];
}

- (BOOL)isEqual:(ShortestPathStep *)other
{
	return GridLocationEqualToLocation(self.location, other.location);
}

- (int)fScore
{
	return self.gScore + self.hScore;
}
@end
