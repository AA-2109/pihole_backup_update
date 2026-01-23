# noinspection Pylint
class ConfigurationError(Exception):
    """Raised when a configuration file is not found."""



class ConfValidationError(ConfigurationError):
    """Raised when a configuration file is invalid."""



class PiHoleError(Exception):
    """Base exception for all Pi-hole related errors."""



class PiHoleAPIError(PiHoleError):
    """Raised when a Pi-hole API fails."""



class PiHoleBackupError(PiHoleError):
    """Raised when a Pi-hole teleport backup fails."""



class PiHoleGravityUpdateError(PiHoleError):
    """Raised when a Pi-hole Gravity Update fails."""
