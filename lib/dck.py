import docker


class CLIDocker:
    def __init__(self, image_name: str, command: str):
        self.client = docker.from_env()
        # flags: https://docs.docker.com/engine/reference/commandline/run/
        self.image_name = image_name
        self.command = command
        self.container = None
        self.container_id = None

    def build(self):
        self.container = self.client.containers.run(
            self.image_name, command=["sh", "-c", self.command], detach=True
        )

    def logs(self) -> list[str]:
        for line in self.container.logs(stream=True):
            if not line:
                continue
            yield line.strip().decode("utf-8")
