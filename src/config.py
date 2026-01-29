from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
import yaml
from pathlib import Path
import os


class ServerSettings(BaseSettings):
    """Server configuration"""
    host: str = "127.0.0.1"
    port: int = 32001
    mcp_path: str = "/data/api/mcp"
    app_id: str = "test_app"  # Default app_id

    model_config = SettingsConfigDict(
        env_prefix="SERVER_",
        env_nested_delimiter="__",
        case_sensitive=False
    )


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
        """Load settings from YAML file, then apply environment variables"""
        config_file = Path(yaml_path)
        config_data = {}
        
        if config_file.exists():
            with open(config_file, "r") as f:
                config_data = yaml.safe_load(f) or {}

        # Create settings - Pydantic will automatically apply env vars
        # because Settings extends BaseSettings with env_file support
        server_config = config_data.get("server", {})
        cache_config = config_data.get("cache", {})
        backend_config = config_data.get("backend", {})
        logging_config = config_data.get("logging", {})

        return cls(
            server=ServerSettings(**server_config),
            cache=CacheSettings(**cache_config),
            backend=BackendSettings(**backend_config),
            logging=LoggingSettings(**logging_config)
        )

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings entirely from environment variables (no YAML)"""
        return cls()
