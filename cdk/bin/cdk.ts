#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { CatsVsDogsStack } from '../lib/catsVsDogsStack';

const app = new cdk.App();
new CatsVsDogsStack(app, 'CdkStack', {
    env: {
        region: 'eu-west-2',
        account: '089953642441',
      },
});
