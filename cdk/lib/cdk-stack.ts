import * as cdk from '@aws-cdk/core';
import * as catsvsdogs_service from './catsvsdogs_service';


export class CdkStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new catsvsdogs_service.CatsVsDogsService(this, 'CatsVsDogs');

  }
}
