import * as path from "path";
import * as core from "@aws-cdk/core";
import * as apigateway from "@aws-cdk/aws-apigateway";
import * as lambda from "@aws-cdk/aws-lambda";
import * as s3 from "@aws-cdk/aws-s3";
import * as route53 from '@aws-cdk/aws-route53';
import * as targets from '@aws-cdk/aws-route53-targets';
import * as acm from '@aws-cdk/aws-certificatemanager';
import * as ecr from '@aws-cdk/aws-ecr';
import { Duration } from "@aws-cdk/core";


const customDomainName='catsvsdogs-dev.goatsinlace.com';
const r53ZoneId='Z075628926D8WBRJD6EIJ';
const versionId='1.2.3.4';

export class CatsVsDogsService extends core.Construct {
  constructor(scope: core.Construct, id: string) {
    super(scope, id);

    // Bucket to store the trained model in plus zipfile of site-packages
    const bucket = new s3.Bucket(this, "CatsVsDogsData");

    // See https://docs.aws.amazon.com/cdk/api/latest/docs/aws-lambda-readme.html#filesystem-access
    // Get hold of the default VPC
    // const vpc = ec2.Vpc.fromLookup(this, 'DefaultVPC', {isDefault: true});

    const dockerfile = path.join(__dirname, "../docker");

    // Get the docker repo holding the container images
    const dockerRepo = ecr.Repository.fromRepositoryName(this, 'DockerRepo', 'cats-vs-dogs-model');
    // Create AWS Lambda function afrom ECR image
    const model_handler = new lambda.DockerImageFunction(this, "ModelHandler", {
      code: lambda.DockerImageCode.fromEcr(dockerRepo, {tag: "latest"}),
      environment: {
        BUCKETNAME: bucket.bucketName
      },
      memorySize: 256,
      timeout: Duration.seconds(15)
    });

    // The lambda needs access to the S3 bucket
    bucket.grantReadWrite(model_handler);

    // Get hold of the hosted zone which has previously been created
    const zone = route53.HostedZone.fromHostedZoneAttributes(this, 'CatsVsDogsR53Zone', {
      zoneName: customDomainName,
      hostedZoneId: r53ZoneId,
    });

    // Create the cert for the gateway.
    // Usefully, this writes the DNS Validation CNAME records to the R53 zone,
    // which is great as normal Cloudformation doesn't do that.
    const acmCertificateForCustomDomain = new acm.DnsValidatedCertificate(this, 'Certificate', {
      domainName: `api.${customDomainName}`,
      hostedZone: zone,
      validation: acm.CertificateValidation.fromDns(zone),
    });

    // Create the custom domain
    const customDomain = new apigateway.DomainName(this, 'CustomDomainName', {
      domainName: `api.${customDomainName}`,
      certificate: acmCertificateForCustomDomain,
      endpointType: apigateway.EndpointType.REGIONAL,
      securityPolicy: apigateway.SecurityPolicy.TLS_1_2
    });

    // This is the API Gateway which then calls the lambda.
    const api = new apigateway.RestApi(this, "catsvsdogs-api", {
      restApiName: "CatsVsDogs Service",
      description: "This service uses a CNN to determine a picture of a cat vs a dog.",
      deploy: false // create the deployment below
    });

    // By default CDK creates a deployment and a "prod" stage.  That means the URL is something like
    // https://2z2ockh6g5.execute-api.eu-west-2.amazonaws.com/prod/
    // We want to create the stage to match the version id.
    // Semantic versioning has dots as separators but this is invalid in a URL
    // so replace the dots with underscores first.
    const versionIdForURL = versionId.replace(/\./g, '_');
    const apiGatewayDeployment = new apigateway.Deployment(this, 'ApiGatewayDeployment', {
      api: api
    });
    const modelStage = new apigateway.Stage(this, 'ModelStage', {
      deployment: apiGatewayDeployment,
      loggingLevel: apigateway.MethodLoggingLevel.INFO,
      dataTraceEnabled: true,
      stageName: versionIdForURL
    })

    // Connect the API to the model lambda
    const modelLambdaIntegration = new apigateway.LambdaIntegration(model_handler, {
      requestTemplates: { "application/json": '{ "statusCode": "200" }' }
    });
    const modelResource = api.root.addResource('model');
    modelResource.addMethod("GET", modelLambdaIntegration);

    // Create the R53 "A" record to map from the custom domain to the actual API URL
    new route53.ARecord(this, 'CustomDomainAliasRecord', {
      recordName: `api.${customDomainName}`,
      zone: zone,
      target: route53.RecordTarget.fromAlias(new targets.ApiGatewayDomain(customDomain))
    });
    // And path mapping to the API
    customDomain.addBasePathMapping(api, { basePath: `${versionIdForURL}`, stage: modelStage });

    // Create an endpoint in the default VPC so the lambdas can access S3
    // const S3Endpoint = vpc.addGatewayEndpoint('S3Endpoint', {
    //   service: ec2.GatewayVpcEndpointAwsService.S3,
    // });
  }
}