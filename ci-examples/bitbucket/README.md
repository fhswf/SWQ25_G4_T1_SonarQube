# Bitbucket Pipelines SonarQube Integration

This directory contains Bitbucket Pipelines examples for integrating SonarQube analysis into your CI/CD process.

## 📁 Files Included

- `bitbucket-pipelines.yml` - Complete pipeline with examples for both SonarQube Server and SonarQube Cloud

## 🚀 Quick Setup

1. **Copy the pipeline file** to your repository root as `bitbucket-pipelines.yml`
2. **Configure repository variables** in your Bitbucket repository settings
3. **Enable Pipelines** in your repository settings
4. **Push changes** to trigger the pipeline

## ⚙️ Required Configuration

### For SonarQube Cloud

**Repository Variables (Settings > Pipelines > Repository variables):**
- `SONAR_TOKEN` - Your SonarQube Cloud user token (Secured: ✓)
- `SONAR_HOST_URL` - SonarQube Cloud URL:
  - `https://sonarcloud.io` (for global instance)
  - `https://sonarqube.us` (for US government instance)

### For SonarQube Server

**Repository Variables:**
- `SONAR_TOKEN` - Your SonarQube Server user token (Secured: ✓)
- `SONAR_HOST_URL` - Your SonarQube Server URL (e.g., `https://sonar.company.com`)

## 📋 Pipeline Configuration

### Pipeline Structure
The pipeline includes these steps:

1. **Python environment setup** with dependency installation
2. **Test execution** with coverage reporting
3. **SonarQube analysis** with scanner execution

### Docker Image
The pipeline uses the official Python Docker image:
```yaml
image: python:3.11
```

### Trigger Events
The pipeline runs on:
- Push to `main` and `develop` branches
- Pull requests targeting `main` and `develop` branches

```yaml
pipelines:
  branches:
    main:
      - step: *sonarqube-analysis
    develop:
      - step: *sonarqube-analysis
  pull-requests:
    '**':
      - step: *sonarqube-analysis
```

## 🛠️ Customization Options

### Python Version
Change the Docker image:
```yaml
image: python:3.9  # or python:3.10, python:3.11
```

### Custom Docker Image
Use a custom image with pre-installed tools:
```yaml
image: your-registry/python-sonar:latest
```

### Analysis Parameters
Customize SonarQube analysis by modifying the script section:
```yaml
script:
  - pipe: sonarsource/sonarqube-scan:2.0.0
    variables:
      SONAR_HOST_URL: $SONAR_HOST_URL
      SONAR_TOKEN: $SONAR_TOKEN
      EXTRA_ARGS: >
        -Dsonar.projectKey=$BITBUCKET_REPO_FULL_NAME
        -Dsonar.sources=src/
        -Dsonar.tests=tests/
        -Dsonar.python.coverage.reportPaths=coverage.xml
        -Dsonar.qualitygate.wait=true
```

### Quality Gate Enforcement
To fail the pipeline when Quality Gate fails:
```yaml
EXTRA_ARGS: >
  -Dsonar.qualitygate.wait=true
```

## 🔧 Advanced Configuration

### Using SonarQube Pipe
Bitbucket provides an official SonarQube pipe:
```yaml
- pipe: sonarsource/sonarqube-scan:2.0.0
  variables:
    SONAR_HOST_URL: $SONAR_HOST_URL
    SONAR_TOKEN: $SONAR_TOKEN
    EXTRA_ARGS: '-Dsonar.sources=src/'
```

### Manual Scanner Setup
Alternative approach using SonarScanner CLI:
```yaml
script:
  - apt-get update && apt-get install -y wget unzip
  - wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
  - unzip sonar-scanner-cli-4.8.0.2856-linux.zip
  - export PATH=$PATH:$(pwd)/sonar-scanner-4.8.0.2856-linux/bin
  - sonar-scanner
```

### Parallel Pipeline Steps
Run tests and analysis in parallel:
```yaml
pipelines:
  branches:
    main:
      - parallel:
        - step:
            name: Run Tests
            script:
              - pip install -r requirements.txt
              - python -m pytest tests/ --cov=src --cov-report=xml
            artifacts:
              - coverage.xml
        - step:
            name: Security Scan
            script:
              - pip install bandit
              - bandit -r src/ -f json -o bandit-report.json
            artifacts:
              - bandit-report.json
      - step:
          name: SonarQube Analysis
          script:
            - pipe: sonarsource/sonarqube-scan:2.0.0
```

### Conditional Execution
Run SonarQube only on specific conditions:
```yaml
- step:
    name: SonarQube Analysis
    condition:
      changesets:
        includePaths:
          - "src/**"
          - "tests/**"
    script:
      - pipe: sonarsource/sonarqube-scan:2.0.0
```

## 🧪 Testing the Integration

### 1. Verify Pipeline Execution
- Check the "Pipelines" section in your Bitbucket repository
- Ensure all steps complete successfully
- Review step logs for any errors

### 2. Check SonarQube Project
- Login to your SonarQube instance
- Verify your project appears with analysis results
- Check that metrics and issues are populated

### 3. Test Pull Request Decoration
- Create a test branch with some code issues
- Create a pull request
- Verify SonarQube comments appear on the PR

## 🔗 Branch Permissions

To enforce quality gates, set up branch permissions:

1. Go to **Repository settings > Branch permissions**
2. Add a restriction for your main branch
3. Select **Restrict pushes** and configure:
   - **Kind of restriction**: Push
   - **Apply restriction to**: Branch name or pattern
   - **Except users**: (leave empty)
   - **Restrict pushes**: ✓ Check that all required builds pass

## 📊 Pipeline Features

### Caching
Enable caching for faster builds:
```yaml
definitions:
  caches:
    sonar: ~/.sonar/cache
    pip: ~/.cache/pip

pipelines:
  branches:
    main:
      - step:
          caches:
            - pip
            - sonar
```

### Artifacts
Share files between pipeline steps:
```yaml
- step:
    name: Run Tests
    script:
      - python -m pytest tests/ --cov=src --cov-report=xml
    artifacts:
      - coverage.xml
      - test-results.xml

- step:
    name: SonarQube Analysis
    script:
      - pipe: sonarsource/sonarqube-scan:2.0.0
    after-script:
      - cat coverage.xml  # Verify artifact is available
```

### Services
Add additional services like databases:
```yaml
- step:
    name: Integration Tests
    services:
      - postgres
    script:
      - python manage.py test

definitions:
  services:
    postgres:
      image: postgres:13
      variables:
        POSTGRES_DB: testdb
        POSTGRES_USER: testuser
        POSTGRES_PASSWORD: testpass
```

## 🔒 Security Best Practices

1. **Use secured variables** for sensitive tokens
2. **Enable IP restrictions** for repository access
3. **Use least privilege principle** for tokens
4. **Regularly rotate access tokens**
5. **Monitor pipeline execution logs**

### Variable Security Settings
In Bitbucket repository settings:
```
Settings > Pipelines > Repository variables

Name: SONAR_TOKEN
Value: [your-token]
Secured: ✓ (checked)
```

## 📚 Documentation Links

- [Bitbucket Pipelines Documentation](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)
- [SonarQube Server Bitbucket Integration](https://docs.sonarsource.com/sonarqube-server/latest/devops-platform-integration/bitbucket-integration/)
- [SonarQube Cloud Bitbucket Integration](https://docs.sonarsource.com/sonarqube-cloud/getting-started/bitbucket/)
- [SonarQube Pipe for Bitbucket](https://bitbucket.org/sonarsource/sonarqube-scan/)

## 🐛 Troubleshooting

### Common Issues

**Pipeline fails with "pipe not found":**
- Ensure you're using the correct pipe name: `sonarsource/sonarqube-scan:2.0.0`
- Check that the pipe version exists
- Verify your Bitbucket account has access to Atlassian Marketplace

**Authentication errors:**
- Verify `SONAR_TOKEN` variable is correctly set and secured
- Check token permissions in SonarQube
- Ensure `SONAR_HOST_URL` is accessible from Bitbucket Pipelines

**Analysis fails with memory errors:**
- Increase pipeline memory allocation:
```yaml
- step:
    name: SonarQube Analysis
    size: 2x  # Use 2x memory (4GB instead of 2GB)
```

**Coverage reports not found:**
- Ensure coverage.xml is generated in the correct location
- Check that artifacts are passed between steps
- Verify pytest-cov configuration

### Debug Mode
Enable verbose logging:
```yaml
- pipe: sonarsource/sonarqube-scan:2.0.0
  variables:
    SONAR_HOST_URL: $SONAR_HOST_URL
    SONAR_TOKEN: $SONAR_TOKEN
    EXTRA_ARGS: '-Dsonar.verbose=true'
```

### Testing Connectivity
Add a test step to verify connectivity:
```yaml
- step:
    name: Test SonarQube Connectivity
    script:
      - curl -u $SONAR_TOKEN: $SONAR_HOST_URL/api/system/status
      - echo "Connection successful"
```

## 💡 Best Practices

1. **Use specific pipe versions** for reproducible builds
2. **Implement proper caching** to speed up pipeline execution
3. **Set up email notifications** for pipeline failures
4. **Use deployment environments** for different stages
5. **Implement parallel steps** where possible to reduce execution time
6. **Monitor pipeline minutes usage** for cost management
7. **Use build status badges** to show pipeline health
8. **Regularly update dependencies** and pipe versions

## 🚀 Performance Optimization

### Memory Configuration
```yaml
- step:
    name: SonarQube Analysis
    size: 2x  # 4GB memory
    script:
      - export SONAR_SCANNER_OPTS="-Xmx3072m"
      - pipe: sonarsource/sonarqube-scan:2.0.0
```

### Selective Analysis
Only run analysis when relevant files change:
```yaml
- step:
    name: SonarQube Analysis
    condition:
      changesets:
        includePaths:
          - "src/**/*.py"
          - "tests/**/*.py"
          - "requirements.txt"
          - "sonar-project.properties"
```

### Build Time Optimization
```yaml
definitions:
  caches:
    pip: ~/.cache/pip
    sonar: ~/.sonar/cache
    node: node_modules

- step:
    name: Fast SonarQube Analysis
    caches:
      - pip
      - sonar
    script:
      - pip install --cache-dir ~/.cache/pip -r requirements.txt
      - pipe: sonarsource/sonarqube-scan:2.0.0
```