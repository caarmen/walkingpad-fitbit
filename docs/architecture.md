
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
        display
        entities
        monitoring
    end
    subgraph interfaceadapters
        cli
        fitbit
        restapi
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
        treadmillcontroller
        remoterepository
        subgraph display
            base
            factory
            formatter
            json
            plaintext
            richtext
        end
        subgraph entities
            activity
            event
        end
        subgraph monitoring
            eventhandler
            monitor
        end
    end
    subgraph interfaceadapters
        subgraph cli
            logincli
        end
        subgraph fitbit
            fitbitemoterepository["remoterepository"]
        end
        subgraph restapi
            server
            treadmillbp
        end
        subgraph walkingpad
            walkingpadtreadmillcontroller["treadmillcontroller"]
            device
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
