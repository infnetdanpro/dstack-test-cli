import click

from lib.aws import AWSLogs
from lib.dck import CLIDocker


@click.command()
@click.option("--docker-image", help="Docker image name", required=True)
@click.option(
    "--bash-command", help="Command for run inside the container", required=True
)
@click.option("--aws-cloudwatch-group", help="AWS Cloudwatch Group", required=True)
@click.option("--aws-cloudwatch-stream", help="AWS Cloudwatch Stream", required=True)
@click.option("--aws-access-key-id", help="AWS Access Key ID", required=True)
@click.option("--aws-secret-access-key", help="AWS Secret Access Key", required=True)
@click.option("--aws-region", help="AWS Region", default="us-west-2")
def main(
    docker_image: str,
    bash_command: str,
    aws_cloudwatch_group: str,
    aws_cloudwatch_stream: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    aws_region: str,
):
    # prepare logger
    aws_logger = AWSLogs(
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        group_name=aws_cloudwatch_group,
        stream_name=aws_cloudwatch_stream,
    )
    docker = CLIDocker(image_name=docker_image, command=bash_command)
    docker.build()
    for message in docker.logs():
        if not message:
            continue
        aws_logger.save_logs(message=message)


if __name__ == "__main__":
    main()
