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
skip folder `venv`
```bash
 tree -I "venv, __pycache__, .pytest_cache"
 ```