import * as core from "@aws-cdk/core";
import * as ecr from "@aws-cdk/aws-ecr";

class ECR extends core.Construct {
  constructor(scope: core.Construct, id: string) {
    super(scope, id);

    const repository = new ecr.Repository(this, 'Repo', {
      repositoryName: "cats-vs-dogs-model",
      imageScanOnPush: true
    });
  }
}

export class ECRStack extends core.Stack {
  constructor(scope: core.Construct, id: string, props?: core.StackProps) {
    super(scope, id, props);

    new ECR(this, 'ECR');
  }
}
