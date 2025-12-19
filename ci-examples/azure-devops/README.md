# Azure DevOps SonarQube Integration

This directory contains Azure DevOps pipeline examples for integrating SonarQube analysis into your CI/CD process.

## 📁 Files Included

- `azure-pipelines.yml` - Complete pipeline with examples for both SonarQube Server and SonarQube Cloud

## 🚀 Quick Setup

1. **Copy the pipeline file** to your repository root as `azure-pipelines.yml`
2. **Install SonarQube extensions** in your Azure DevOps organization
3. **Configure service connections** and variables
4. **Create a new pipeline** in Azure DevOps pointing to your YAML file

## 🔧 Required Extensions

Install these extensions in your Azure DevOps organization:

### For SonarQube Server
- [SonarQube Extension](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarqube)

### For SonarQube Cloud  
- [SonarCloud Extension](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarcloud)

## ⚙️ Required Configuration

### For SonarQube Cloud

**Service Connection:**
1. Go to **Project Settings > Service connections**
2. Create **New service connection > SonarCloud**
3. Authenticate with your SonarCloud account
4. Name it `SonarCloudServiceConnection`

**Pipeline Variables:**
- No additional variables needed (handled by service connection)

### For SonarQube Server

**Service Connection:**
1. Go to **Project Settings > Service connections**  
2. Create **New service connection > SonarQube**
3. Configure:
   - **Server URL**: Your SonarQube Server URL
   - **Token**: Your SonarQube Server user token
4. Name it `SonarQubeServiceConnection`

**Pipeline Variables:**
- `SONAR_HOST_URL` - Your SonarQube Server URL (optional, can be in service connection)

## 📋 Pipeline Configuration

### Trigger Events
The pipeline is configured to run on:
- Push to `main` and `develop` branches
- Pull requests targeting `main` and `develop` branches

```yaml
trigger:
  branches:
    include:
    - main
    - develop

pr:
  branches:
    include:
    - main
    - develop
```

### Pipeline Structure
The pipeline includes these key steps:

1. **Python setup** with version specification
2. **Dependency installation** with pip caching
3. **Test execution** with coverage reporting
4. **SonarQube preparation** (download scanner, configure project)
5. **SonarQube analysis** (code scanning)
6. **SonarQube publish** (upload results and check quality gate)

## 🛠️ Customization Options

### Python Version
Modify the Python version:
```yaml
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'  # Change to your preferred version
```

### Analysis Parameters
Customize SonarQube analysis in the prepare task:
```yaml
- task: SonarQubePrepare@5
  inputs:
    SonarQube: 'SonarQubeServiceConnection'
    scannerMode: 'CLI'
    configMode: 'manual'
    cliProjectKey: 'your-project-key'
    cliProjectName: 'Your Project Name'
    extraProperties: |
      sonar.sources=src/
      sonar.tests=tests/
      sonar.python.coverage.reportPaths=coverage.xml
      sonar.qualitygate.wait=true
```

### Quality Gate Enforcement
To fail the pipeline when Quality Gate fails:
```yaml
extraProperties: |
  sonar.qualitygate.wait=true
```

### Agent Pool
Specify a different agent pool:
```yaml
pool:
  vmImage: 'windows-latest'  # or 'macos-latest'
```

## 🧪 Testing the Integration

### 1. Verify Pipeline Execution
- Check the pipeline run in Azure DevOps
- Ensure all tasks complete successfully
- Verify SonarQube analysis uploads results

### 2. Check SonarQube Project
- Login to your SonarQube instance
- Verify your project appears with analysis results
- Check that metrics and issues are populated

### 3. Test Pull Request Decoration
- Create a test branch with some code issues
- Create a pull request
- Verify SonarQube comments appear on the PR

## 🔗 Branch Policies

To enforce quality gates, set up branch policies:

1. Go to **Repos > Branches** in your project
2. Select your main branch and click **Branch policies**
3. Add **Build validation** policy
4. Select your SonarQube pipeline
5. Enable **Required** status

## 📊 Pipeline Variables and Parameters

### Environment Variables
Common variables you can set:

```yaml
variables:
  pythonVersion: '3.11'
  buildConfiguration: 'Release'
  vmImageName: 'ubuntu-latest'
```

### Runtime Parameters
Add parameters for flexibility:

```yaml
parameters:
- name: runSonarQube
  displayName: 'Run SonarQube Analysis'
  type: boolean
  default: true

- name: sonarQubeProjectKey
  displayName: 'SonarQube Project Key'
  type: string
  default: 'default-project-key'
```

## 🔒 Security Best Practices

1. **Use service connections** for authentication
2. **Store secrets in Azure Key Vault** for sensitive data
3. **Limit pipeline permissions** to required resources only
4. **Use managed identities** when possible
5. **Regularly rotate tokens** used in service connections

## 📚 Documentation Links

- [Azure DevOps Pipeline Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [SonarQube Extension for Azure DevOps](https://docs.sonarsource.com/sonarqube-server/latest/devops-platform-integration/azure-devops-integration/installing-the-extension/)
- [SonarCloud Extension for Azure DevOps](https://docs.sonarsource.com/sonarqube-cloud/getting-started/azure-devops/)

## 🐛 Troubleshooting

### Common Issues

**Pipeline fails with extension not found:**
- Ensure SonarQube/SonarCloud extension is installed in your organization
- Check that you're using the correct task version

**Authentication errors:**
- Verify service connection configuration
- Check token permissions and expiration
- Ensure service connection name matches pipeline YAML

**Analysis fails with "project not found":**
- Verify project key exists in SonarQube
- Check service connection has access to the project
- Ensure organization/project permissions are correct

**Quality Gate not enforced:**
- Add `sonar.qualitygate.wait=true` to extraProperties
- Verify Quality Gate is configured in SonarQube project
- Check that the pipeline waits for analysis completion

### Debug Tips

**Enable verbose logging:**
```yaml
extraProperties: |
  sonar.verbose=true
```

**Check task logs:**
- Click on failed tasks in pipeline run
- Review detailed logs for specific error messages
- Check SonarQube server logs if needed

## 💡 Best Practices

1. **Use YAML pipelines** instead of classic editor for version control
2. **Implement proper branching strategy** with appropriate triggers
3. **Cache dependencies** to improve build performance
4. **Use templates** for reusable pipeline components
5. **Monitor pipeline performance** and optimize as needed
6. **Set up proper notifications** for build failures
7. **Use variable groups** for shared configuration across pipelines