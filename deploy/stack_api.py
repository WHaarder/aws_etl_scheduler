from os.path import join, dirname, abspath
from json import dumps

from aws_cdk.core import Stack, Construct, Duration
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
import aws_cdk.aws_iam as iam


_dirname = join(dirname(abspath(__file__)), "..")

LAMBDA_MEMORY_SIZE = 512
LAMBDA_TIMEOUT_SEC = 360

SECRET_ARN = ""


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        backend = DockerImageFunction(
            self,
            "ModelBackend",
            code=DockerImageCode.from_image_asset(join(_dirname, "lambda")),
            timeout=Duration.seconds(LAMBDA_TIMEOUT_SEC),
            memory_size=LAMBDA_MEMORY_SIZE,
        )
        backend.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "secretsmanager:GetResourcePolicy",
                    "secretsmanager:GetSecretValue",
                    "secretsmanager:DescribeSecret",
                    "secretsmanager:ListSecretVersionIds",
                ],
                resources=[SECRET_ARN],
            )
        )
        backend.add_to_role_policy(
            iam.PolicyStatement(
                actions=["secretsmanager:ListSecrets"],
                resources=["*"],
            )
        )
        # fn: lambda.Function
        input = events.RuleTargetInput.from_object({"test": "test1!"})
        rule = events.Rule(
            self, "Schedule Rule", schedule=events.Schedule.cron(minute="0", hour="4")
        )
        rule.add_target(targets.LambdaFunction(backend, event=input))
