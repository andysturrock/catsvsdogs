#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { ECRStack } from '../lib/ECRStack';
import { CatsVsDogsStack } from '../lib/catsVsDogsStack';

const app = new cdk.App();

new ECRStack(app, 'ECRStack', {
  env: {
      region: 'eu-west-1',
      account: '089953642441',
    },
});

new CatsVsDogsStack(app, 'CatsVsDogsStack', {
    env: {
        region: 'eu-west-1',
        account: '089953642441',
      },
});