# Tests

## Development tip

`./sandbox dev up` - is how to run without respect to accurate block time

### Tip to map `./scripts/escrow` directory into the sandbox after launching with `./sandbox enter algod`

add the following to `docker-compose.yml` in the sandbox project

```
services:
    algod:
        volumes:
            - type: bind
              source: ../<PROJECT_WHERE_SMART_CONTRACTS_ARE_DEVELOPED>
              target: /data
```

## 

`./sandbox up` - is how to run with accuracte block times

##

`./sandbox enter algod`

