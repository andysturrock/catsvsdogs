import * as core from '@aws-cdk/core';
import * as catsvsdogs_service from './catsVsDogsService';


export class CatsVsDogsStack extends core.Stack {
  constructor(scope: core.Construct, id: string, props?: core.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new catsvsdogs_service.CatsVsDogsService(this, 'CatsVsDogs');

  }
}
