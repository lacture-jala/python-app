### Coverage python code

Install Coverage

```bash
# Install test dependencies if not already done
pip install coverage pytest

# Run tests with coverage
coverage run -m pytest

# Generate XML report for SonarQube
coverage xml

```

skip multiple folder folders `venv`

```bash
tree -I "venv|__pycache__|.pytest_cache"
```

### Configure Jenkins Plugins

- Install:
    -   **ShiningPanda** (Python builds support)
    -   **SonarQube Scanner** for Jenkins
    -   **JUnit** plugin (optional if you generate junit XML reports)
    -   **HTML Publisher** plugin (to show coverage reports)
