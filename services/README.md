# Services

FlaPol Style currently operates no hosted service, daemon, database, queue,
web application or production endpoint.

The Python package and Vale rules are libraries consumed by other projects.
GitHub Actions is an external CI provider, not a service administered here.

Create a service record only if this project later owns a real hosted runtime,
including its target, configuration contract, health check, persistence,
recovery and operational runbook. Do not put consumer-owned services here.
