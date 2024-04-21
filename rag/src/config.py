from pydantic_settings import BaseSettings


class Config(BaseSettings):
    chroma_hostname: str
    chroma_port: int


def get_config() -> Config:
    return Config()  # type: ignore
