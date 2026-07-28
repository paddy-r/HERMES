# rate_sources/__init__.py

import importlib
import pkgutil

for module in pkgutil.iter_modules(__path__):
    importlib.import_module(
        f"{__name__}.{module.name}"
    )
