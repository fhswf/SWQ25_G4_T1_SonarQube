# GitHub Actions SonarQube Integration

This directory contains GitHub Actions workflow examples for integrating SonarQube analysis into your CI/CD pipeline.

## 📁 Files Included

- `sonarqube-analysis.yml` - Complete workflow with examples for both SonarQube Server and SonarQube Cloud

## 🚀 Quick Setup

1. **Copy the workflow file** to your repository's `.github/workflows/` directory
2. **Configure secrets/variables** in your GitHub repository settings
3. **Customize the workflow** for your project needs
4. **Push changes** to trigger the workflow

## ⚙️ Required Configuration

### For SonarQube Cloud

**Repository Secrets (Settings > Secrets and variables > Actions):**
- `SONAR_TOKEN` - Your SonarQube Cloud token

**Repository Variables:**
- `SONAR_HOST_URL` - SonarQube URL
  SonarQube Cloud URL options:
  - `https://sonarcloud.io` (for European hosted instance)
  - `https://sonarqube.us` (for US hosted instance)

### For SonarQube Server

**Repository Secrets:**
- `SONAR_TOKEN` - Your SonarQube Server token

**Repository Variables:**
- `SONAR_HOST_URL` - Your SonarQube Server URL (e.g., `https://sonar.company.com`)

## 🔧 Workflow Configuration

### Trigger Events
The workflow is configured to run on:
- Push to `main` and `develop` branches
- Pull requests targeting `main` and `develop` branches

To customize triggers, modify the `on:` section:

```yaml
on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]
```

### SonarQube Scanner Action
The workflow uses the official `sonarqube-scan-action@v6`:
- Automatically uses the latest v6.x.x version
- Supports both SonarQube Server and Cloud
- Includes built-in quality gate checking

### Quality Gate Enforcement
To fail the pipeline when Quality Gate fails, uncomment this line in the workflow:
```yaml
# -Dsonar.qualitygate.wait=true
```

## 📋 Workflow Features

- **Shallow fetch disabled** (`fetch-depth: 0`) for accurate blame information
- **Python setup** with dependency caching
- **Test execution** with coverage reporting
- **SonarQube analysis** with configurable parameters
- **Quality Gate integration** (optional pipeline failure)

## 🛠️ Customization Options

### Analysis Parameters
Modify the `args` section to customize analysis:

```yaml
with:
  args: >
    -Dsonar.verbose=true
    -Dsonar.sources=src/
    -Dsonar.tests=tests/
    -Dsonar.python.coverage.reportPaths=coverage.xml
    -Dsonar.qualitygate.wait=true
```

### Branch Strategy
For different branch strategies, update the trigger and add branch-specific logic:

```yaml
on:
  push:
    branches: [ "main", "release/*" ]
  pull_request:
    branches: [ "main" ]
```

### Matrix Builds
For multi-version testing:

```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, "3.10", "3.11"]
```

## 🧪 Testing the Integration

### 1. Verify Workflow Execution
- Check the "Actions" tab in your GitHub repository
- Ensure the workflow runs without errors
- Verify SonarQube analysis completes successfully

### 2. Check SonarQube Project
- Login to your SonarQube instance
- Verify your project appears with analysis results
- Check that metrics and issues are populated

### 3. Test Pull Request Decoration
- Create a test branch with some code issues
- Open a pull request
- Verify SonarQube comments appear on the PR

## 🔗 Branch Protection Rules

To enforce quality gates, set up branch protection rules:

1. Go to **Settings > Branches** in your repository
2. Add a rule for your main branch
3. Enable **Require status checks to pass**
4. Select the SonarQube status check

## 📚 Documentation Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [SonarQube Server GitHub Integration](https://docs.sonarsource.com/sonarqube-server/latest/devops-platform-integration/github-integration/introduction/)
- [SonarQube Cloud GitHub Integration](https://docs.sonarsource.com/sonarqube-cloud/getting-started/github/)
- [Official SonarQube Scan Action](https://github.com/marketplace/actions/official-sonarqube-scan)

## 🐛 Troubleshooting

### Common Issues

**Workflow fails with "shallow repository" error:**
- Ensure `fetch-depth: 0` is set in the checkout action

**SonarQube analysis fails with authentication error:**
- Verify `SONAR_TOKEN` secret is correctly set
- Check that the token has the required permissions

**Quality Gate status not appearing:**
- Ensure your SonarQube project has a Quality Gate configured
- Verify DevOps platform integration is set up in SonarQube

**PR decoration not working:**
- Check SonarQube project settings for GitHub integration
- Verify repository permissions and webhook configuration

### Debug Mode
Enable verbose logging by adding:
```yaml
-Dsonar.verbose=true
```

## 💡 Best Practices

1. **Use secrets for sensitive data** - Never hardcode tokens in workflows
2. **Pin action versions** - Use specific versions for production workflows
3. **Cache dependencies** - Improve workflow performance with caching
4. **Fail fast** - Use quality gates to catch issues early
5. **Monitor workflow usage** - Track Actions minutes usage for cost management
