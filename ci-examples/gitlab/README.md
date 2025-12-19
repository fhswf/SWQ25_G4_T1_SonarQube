# GitLab CI SonarQube Integration

This directory contains GitLab CI pipeline examples for integrating SonarQube analysis into your CI/CD process.

## 📁 Files Included

- `.gitlab-ci.yml` - Complete pipeline with examples for both SonarQube Server and SonarQube Cloud

## 🚀 Quick Setup

1. **Copy the pipeline file** to your repository root as `.gitlab-ci.yml`
2. **Configure CI/CD variables** in your GitLab project settings
3. **Customize the pipeline** for your project needs
4. **Push changes** to trigger the pipeline

## ⚙️ Required Configuration

### For SonarQube Cloud

**Project Variables (Settings > CI/CD > Variables):**
- `SONAR_TOKEN` - Your SonarQube Cloud user token (Type: Variable, Protected: Yes, Masked: Yes)
- `SONAR_HOST_URL` - SonarQube Cloud URL (Type: Variable):
  - `https://sonarcloud.io` (for global instance)
  - `https://sonarqube.us` (for US government instance)

### For SonarQube Server

**Project Variables:**
- `SONAR_TOKEN` - Your SonarQube Server user token (Type: Variable, Protected: Yes, Masked: Yes)
- `SONAR_HOST_URL` - Your SonarQube Server URL (Type: Variable, e.g., `https://sonar.company.com`)

## 📋 Pipeline Configuration

### Pipeline Structure
The pipeline includes these stages:

1. **test** - Run tests and generate coverage reports
2. **sonarqube-check** - Perform SonarQube analysis
3. **sonarqube-vulnerability-report** - Generate vulnerability reports (SonarQube Cloud only)

### Default Image
The pipeline uses the official Python Docker image:
```yaml
image: python:3.11
```

### Trigger Events
The pipeline runs on:
- All branch pushes
- Merge requests
- Manual pipeline triggers

To customize triggers, modify the rules:
```yaml
rules:
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  - if: $CI_COMMIT_BRANCH == "develop"
```

## 🛠️ Customization Options

### Python Version
Change the Docker image:
```yaml
image: python:3.9  # or python:3.10, python:3.11
```

### Analysis Parameters
Customize SonarQube analysis by modifying the script section:
```yaml
script:
  - sonar-scanner
    -Dsonar.projectKey=$CI_PROJECT_PATH_SLUG
    -Dsonar.sources=src/
    -Dsonar.tests=tests/
    -Dsonar.python.coverage.reportPaths=coverage.xml
    -Dsonar.qualitygate.wait=true
```

### Quality Gate Enforcement
To fail the pipeline when Quality Gate fails:
```yaml
-Dsonar.qualitygate.wait=true
```

### Caching
The pipeline includes pip caching for faster builds:
```yaml
cache:
  paths:
    - ~/.cache/pip/
```

Add SonarQube scanner caching:
```yaml
cache:
  paths:
    - ~/.cache/pip/
    - .sonar/cache/
```

## 🔧 Advanced Configuration

### Multiple Python Versions
Create a matrix build for multiple Python versions:
```yaml
test:
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.8", "3.9", "3.10", "3.11"]
  image: python:$PYTHON_VERSION
  script:
    - pip install -r requirements.txt
    - python -m pytest tests/ --cov=src --cov-report=xml
```

### Conditional Analysis
Run SonarQube only on specific branches:
```yaml
sonarqube-check:
  stage: sonarqube-check
  image: 
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

### Integration with GitLab Security
Enable GitLab security features:
```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
```

## 🧪 Testing the Integration

### 1. Verify Pipeline Execution
- Check the "CI/CD > Pipelines" section in your GitLab project
- Ensure all jobs complete successfully
- Review job logs for any errors

### 2. Check SonarQube Project
- Login to your SonarQube instance
- Verify your project appears with analysis results
- Check that metrics and issues are populated

### 3. Test Merge Request Decoration
- Create a test branch with some code issues
- Open a merge request
- Verify SonarQube comments appear on the MR

## 🔗 Merge Request Integration

### Enable MR Decoration
In SonarQube project settings:
1. Go to **Administration > General Settings > DevOps Platform Integration**
2. Configure GitLab integration with:
   - GitLab URL
   - Personal Access Token
   - Repository identifier

### Push Rules
Set up push rules to enforce quality:
1. Go to **Settings > Repository > Push Rules**
2. Enable quality gate enforcement
3. Configure branch protection rules

## 📊 Pipeline Artifacts and Reports

### Test Coverage Reports
The pipeline generates coverage reports:
```yaml
artifacts:
  reports:
    coverage_report:
      coverage_format: cobertura
      path: coverage.xml
```

### SonarQube Reports (GitLab Ultimate)
For vulnerability reporting:
```yaml
artifacts:
  reports:
    sast: gl-sast-sonarqube-report.json
```

## 🔒 Security Best Practices

1. **Use masked variables** for sensitive tokens
2. **Enable protected variables** for production
3. **Limit variable scope** to specific environments
4. **Use GitLab CI/CD variable hierarchy** appropriately
5. **Regularly rotate access tokens**

### Variable Security Settings
```yaml
# In GitLab UI: Settings > CI/CD > Variables
SONAR_TOKEN:
  Type: Variable
  Environment scope: All
  Protected: Yes
  Masked: Yes
  Expanded: No
```

## 📚 Documentation Links

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [SonarQube Server GitLab Integration](https://docs.sonarsource.com/sonarqube-server/latest/devops-platform-integration/gitlab-integration/)
- [SonarQube Cloud GitLab Integration](https://docs.sonarsource.com/sonarqube-cloud/getting-started/gitlab/)
- [GitLab SAST with SonarQube](https://docs.gitlab.com/ee/user/application_security/sast/#sonarqube)

## 🐛 Troubleshooting

### Common Issues

**Pipeline fails with "sonar-scanner: command not found":**
- Ensure you're using the correct Docker image: `sonarsource/sonar-scanner-cli:latest`
- Check that the image entrypoint is properly configured

**Authentication errors:**
- Verify `SONAR_TOKEN` variable is correctly set and masked
- Check token permissions and expiration in SonarQube
- Ensure `SONAR_HOST_URL` is accessible from GitLab runners

**Analysis fails with network errors:**
- Check GitLab runner network connectivity to SonarQube server
- Verify firewall and proxy settings
- Test connectivity with curl in a test job

**Coverage reports not appearing:**
- Ensure coverage.xml is generated in the correct format
- Check file paths in sonar.python.coverage.reportPaths
- Verify pytest-cov is installed and configured correctly

### Debug Mode
Enable verbose logging:
```yaml
script:
  - sonar-scanner -Dsonar.verbose=true
```

### Testing Connectivity
Add a test job to verify connectivity:
```yaml
test-connectivity:
  stage: test
  image: curlimages/curl:latest
  script:
    - curl -u $SONAR_TOKEN: $SONAR_HOST_URL/api/system/status
  rules:
    - when: manual
```

## 💡 Best Practices

1. **Use specific Docker image tags** for reproducible builds
2. **Implement proper caching** to speed up pipeline execution
3. **Set up notifications** for pipeline failures
4. **Use GitLab environments** for different deployment stages
5. **Implement parallel jobs** where possible to reduce execution time
6. **Use include and extends** for reusable pipeline components
7. **Monitor pipeline performance** and optimize bottlenecks
8. **Follow GitLab CI/CD best practices** for security and maintainability

## 🚀 Performance Optimization

### Parallel Execution
```yaml
test:
  parallel: 3
  script:
    - pytest tests/ --cov=src --cov-append
```

### Selective Pipeline Execution
```yaml
sonarqube-check:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - changes:
        - "src/**/*"
        - "tests/**/*"
```

### Resource Optimization
```yaml
variables:
  SONAR_SCANNER_OPTS: "-Xmx2048m"
  
sonarqube-check:
  tags:
    - high-memory  # Use runners with more memory
```