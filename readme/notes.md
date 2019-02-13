# Architecture

1. all yapsy plugins loaded
1. all hooks and impls are loaded
1. store is activated
    1. store uses hooks to collect reducers, middleware, and subscribers:
    
        ```python
        middlewares = tuple(self.pm.hook.get_middleware())
        ```
    
        use the hook to allow the store to collect your middleware:
    
        ```python
        impl = HookimplMarker("rpack")
        
        
        @middleware
        def loggit(store, next_middleware, action):
            logger.log("DEBUG", f"{action.type} {action.payload}")
            return next_middleware(action)
        
        
        class Logging(IPlugin):
            @staticmethod
            @impl
            def get_middleware():
                return loggit
        ```
    1. next the store is created by combining reducers
        ```python
        combine_reducer(self.pm.hook.get_reducer() [...]
        ```
        therefore if the plugin needs a reducer of its own:
        ```python
            @impl
            def get_reducer(self):
                return config
        ```
        where config is your default reducer (note: the store will gain a root key named after your reducer function!)
    1. finally, subscribers are registered:
        ```python
        for sub in self.pm.hook.subscribe():
            self.the_store.subscribe(sub)
        ```
1. all other plugins are activated.

## Celery

Single function: action dispatcher, which looks for a yapsy plugin based on criteria passed as args.
Plugin runs on activate (?) so we could potentially load plugins based on args, then have an invoke method which accepts some json as its only arg, forwarded from the dispatcher method