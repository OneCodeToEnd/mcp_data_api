from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
import yaml
from pathlib import Path


class ServerSettings(BaseSettings):
    """Server configuration"""
    host: str = "127.0.0.1"
    port: int = 32001
    mcp_path: str = "/data/api/mcp"


class CacheSettings(BaseSettings):
    """Cache configuration"""
    enabled: bool = True
    ttl: int = 3600  # 1 hour in seconds
    type: Literal["memory", "redis"] = "memory"


class BackendSettings(BaseSettings):
    """Backend API configuration"""
    base_url: str = "https://api.example.com"
    api_key: str = ""
    timeout: int = 30

    model_config = SettingsConfigDict(env_prefix="BACKEND_")


class LoggingSettings(BaseSettings):
    """Logging configuration"""
    level: str = "INFO"


class Settings(BaseSettings):
    """Main application settings"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False
    )

    server: ServerSettings = Field(default_factory=ServerSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    backend: BackendSettings = Field(default_factory=BackendSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    @classmethod
    def from_yaml(cls, yaml_path: str = "config/config.yaml") -> "Settings":
        """Load settings from YAML file"""
        config_file = Path(yaml_path)
        if config_file.exists():
            with open(config_file, "r") as f:
                config_data = yaml.safe_load(f)

            return cls(
                server=ServerSettings(**config_data.get("server", {})),
                cache=CacheSettings(**config_data.get("cache", {})),
                backend=BackendSettings(**config_data.get("backend", {})),
                logging=LoggingSettings(**config_data.get("logging", {}))
            )
        return cls()
