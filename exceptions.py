class ConfigurationError(Exception):
    """Raised when a configuration file is not found."""
    pass

class ConfValidationError(ConfigurationError):
    """Raised when a configuration file is invalid."""
    pass


class PiHoleError(Exception):
    """Base exception for all Pi-hole related errors."""
    pass


class PiHoleAPIError(PiHoleError):
    """Raised when a Pi-hole API fails."""
    pass


class PiHoleBackupError(PiHoleError):
    """Raised when a Pi-hole teleport backup fails."""
    pass


class PiHoleGravityUpdateError(PiHoleError):
    """Raised when a Pi-hole Gravity Update fails."""
    pass