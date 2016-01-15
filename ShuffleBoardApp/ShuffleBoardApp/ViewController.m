//
//  ViewController.m
//  ShuffleBoardApp
//
//  Created by Kenneth on 1/14/16.
//  Copyright © 2016 Rhumbix. All rights reserved.
//

#import "ViewController.h"
#import <FastttCamera.h>
#import <AFNetworking.h>
#import "UIImage+Resize.h"

@interface ViewController () <FastttCameraDelegate>
@property (nonatomic, strong) FastttCamera *fastCamera;
@property (nonatomic, strong) NSTimer *timer;
@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    _fastCamera = [FastttCamera new];
    self.fastCamera.delegate = self;
    
    [self fastttAddChildViewController:self.fastCamera];
    self.fastCamera.view.frame = self.view.frame;
    
    self.timer = [NSTimer scheduledTimerWithTimeInterval:10.0f
                                             target:self
                                           selector:@selector(capture)
                                           userInfo:nil
                                            repeats:YES];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)capture {
    [self.fastCamera takePicture];
}

- (void)cameraController:(FastttCamera *)cameraController
didFinishNormalizingCapturedImage:(FastttCapturedImage *)capturedImage
{
    AFHTTPRequestOperationManager *manager = [[AFHTTPRequestOperationManager alloc] initWithBaseURL:[NSURL URLWithString:@"http://ec2-52-53-224-116.us-west-1.compute.amazonaws.com:3000/"]];
    CGSize size = CGSizeMake(512, 512);
    NSData *imageData = UIImageJPEGRepresentation([capturedImage.fullImage resizedImageToFitInSize:size scaleIfSmaller:YES], 1.0);
    AFHTTPRequestOperation *op = [manager POST:@"upload" parameters:nil constructingBodyWithBlock:^(id<AFMultipartFormData> formData) {
        //do not put image inside parameters dictionary as I did, but append it!
        [formData appendPartWithFileData:imageData name:@"file" fileName:@"photo.jpg" mimeType:@"image/jpeg"];
    } success:^(AFHTTPRequestOperation *operation, id responseObject) {
        NSLog(@"Success: %@ ***** %@", operation.responseString, responseObject);
    } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
        NSLog(@"Error: %@ ***** %@", operation.responseString, error);
    }];
    [op start];
}
@end
