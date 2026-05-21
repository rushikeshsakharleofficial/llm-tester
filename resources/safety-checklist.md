# Safety Checklist

Use this checklist before running tests or verification commands.

## Safe by default

These are usually safe in a local/dev repository:

- Read-only file inspection
- Syntax checks
- Unit tests
- Type checks
- Local builds
- Static analysis
- Dry-run validation
- Config parsers
- Container config rendering
- Terraform validate without apply
- Ansible syntax check
- Kubernetes client-side dry run

## Needs caution

Ask whether the target is safe or use dry-run/manual steps before:

- Database migrations
- Database tuning changes
- Service restarts
- Firewall/network changes
- Kernel/sysctl tuning
- Sudo/root commands
- Package installation/removal
- File deletion or recursive writes
- Cloud resource changes
- CI/CD deployment triggers
- Running unknown shell scripts

## Never claim verification if

- The command was not run.
- The command failed.
- The command only checked formatting but not behavior.
- The test environment is missing required services.
- The result depends on production-only resources.

## Required fallback when unsafe

When direct testing is unsafe, provide:

1. Exact dry-run command if available.
2. Exact manual verification steps.
3. Expected successful output.
4. Rollback plan.
5. Remaining risk.
