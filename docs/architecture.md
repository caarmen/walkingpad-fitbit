
# Architecture

## Top-level packages, with top-level package dependencies
```mermaid
flowchart TD
    main
    auth
    domain
    interfaceadapters

    authlib(("authlib"))
    ph4_walkingpad(("ph4<br>walkingpad"))

    main --> auth
    main --> domain
    main --> interfaceadapters

    interfaceadapters --> domain
    interfaceadapters --> auth

    interfaceadapters --> ph4_walkingpad
    auth --> authlib
```

## All packages, with top-level package dependencies
```mermaid
flowchart TD
    main
    auth
    subgraph domain
        entities
    end
    subgraph interfaceadapters
        cli
        fitbit
        walkingpad
    end

    authlib(("authlib"))
    ph4_walkingpad(("ph4<br>walkingpad"))

    main --> auth
    main --> domain
    main --> interfaceadapters

    interfaceadapters --> domain
    interfaceadapters --> auth

    interfaceadapters --> ph4_walkingpad
    auth --> authlib
```

## Packages and modules, with top-level package dependencies
```mermaid
flowchart TD
    main
    subgraph auth
        client
        config
        login
        storage
    end
    subgraph domain
        eventhandler
        remoterepository
        subgraph entities
            activity
            event
        end
    end
    subgraph interfaceadapters
        subgraph cli
            logincli
        end
        subgraph fitbit
            fitbitemoterepository["remoterepository"]
        end
        subgraph walkingpad
            monitor
        end
    end

    authlib(("authlib"))
    ph4_walkingpad(("ph4<br>walkingpad"))

    main --> auth
    main --> domain
    main --> interfaceadapters

    interfaceadapters --> domain
    interfaceadapters --> auth
    interfaceadapters --> ph4_walkingpad
    auth --> authlib
```
