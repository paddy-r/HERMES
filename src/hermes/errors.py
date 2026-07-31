class HermesError(Exception):
    """
    Base class for all Hermes exceptions.
    """

    def __init__(self, message=""):
        super().__init__(message)
        self.message = message


class VerificationError(HermesError):
    """
    Raised when verification fails.
    """
    pass


class PopulationError(HermesError):
    """
    Raised when a population-related runtime error occurs.
    """
    pass


class DomainError(HermesError):
    """
    Raised when a domain-related runtime error occurs.
    """
    pass


class TransitionError(HermesError):
    """
    Raised when a transition-related runtime error occurs.
    """
    pass


class MissingnessError(HermesError):
    """
    Raised when uncontrolled missingness is foun in occurs.
    """
    pass