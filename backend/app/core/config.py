from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = ""

    # SMTP — optional, required for email sending
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    # Domain used to build per-user SMTP auth address, e.g. "renr.grupoepi.es"
    # Result: pespinosa@prensaiberica.es → pespinosa@renr.grupoepi.es
    SMTP_AUTH_DOMAIN: str = ""

    # Sports events — API key used by n8n to POST daily sport events
    SPORTS_API_KEY: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
