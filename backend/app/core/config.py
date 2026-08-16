from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "SupportFlow"
    app_env: str = "development"
    debug: bool = True

    # API
    api_v1_prefix: str = "/api"

    # Frontend / CORS
    frontend_url: str = "http://localhost:5173"
    cors_origins: str = "http://localhost:5173"

    # Database
    database_url: str = "sqlite:///./supportflow.db"

    # Logging / Hosts
    log_level: str = "INFO"
    allowed_hosts: str = "localhost,127.0.0.1"

    # Authentication
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # OTP
    otp_expire_minutes: int = 10
    otp_max_attempts: int = 5

    # SLA / Scheduler
    sla_check_interval_seconds: int = 60

    # Testing
    testing: bool = False

    # Email / SMTP
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from_email: str | None = None
    smtp_from_name: str = "SupportFlow"

    @property
    def cors_origin_list(
        self,
    ) -> list[str]:
        return [
            item.strip()
            for item in self.cors_origins.split(",")
            if item.strip()
        ]

    @property
    def allowed_host_list(
        self,
    ) -> list[str]:
        return [
            item.strip()
            for item in self.allowed_hosts.split(",")
            if item.strip()
        ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()