import time
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from boto3 import Session


def create_aws_client(
    aws_region: str, aws_access_key_id: str, aws_secret_access_key: str
) -> "Session":
    # class fabric
    client: "Session" = boto3.client(
        "logs",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    return client


class AWSLogs:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_region: str = "us-west-2",
        group_name: str = "some-test",
        stream_name: str = "some-test-app",
    ):
        self.client = create_aws_client(
            aws_region=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.logGroupName = group_name
        self.logStreamName = stream_name
        self.prepare_group_stream()

    def prepare_group_stream(self):
        group_names = set()
        resp: dict = self.client.describe_log_groups()
        for log_group_record in resp["logGroups"]:
            group_names.add(log_group_record["logGroupName"])

        if self.logGroupName not in group_names:
            self.client.create_log_stream(
                logGroupName=self.logGroupName, logStreamName=self.logStreamName
            )

    def save_logs(self, message):
        self.client.put_log_events(
            logGroupName=self.logGroupName,
            logStreamName=self.logStreamName,
            logEvents=[
                {"timestamp": int(round(time.time() * 1000)), "message": message}
            ],
        )
