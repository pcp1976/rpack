from .plugin_manager import pm
from .store import StoreImpl, StoreSpec

implementations = [StoreImpl]
specs = [StoreSpec]

for Spec in specs:
    pm.add_hookspecs(Spec())

for Implementation in implementations:
    pm.register(Implementation())
