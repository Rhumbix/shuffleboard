//
//  UIImage+UIImage_Resize.h
//  ShuffleBoardApp
//
//  Created by Kenneth on 1/14/16.
//  Copyright © 2016 Rhumbix. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface UIImage(ResizeCategory)
-(UIImage*)resizedImageToSize:(CGSize)dstSize;
-(UIImage*)resizedImageToFitInSize:(CGSize)boundingSize scaleIfSmaller:(BOOL)scale;
@end