Starting with a "Hello World" project is a great way to familiarize yourself with unit testing, GitHub for version control, and Kanban for project management. Below is a step-by-step guide to help you set up a simple project using these tools:

## 1. **Set Up Your Development Environment**

Before you begin, ensure you have the necessary tools installed:

- **Git**: Version control system. [Download Git](https://git-scm.com/downloads)
- **IDE/Text Editor**: Such as VS Code, IntelliJ, or any editor you're comfortable with.
- **Programming Language**: Choose one (e.g., Python, JavaScript, Java). This guide will use **Python** for simplicity.
- **Package Manager**: For Python, `pip` is standard.

## 2. **Create a GitHub Repository**

1. **Sign in to GitHub**: If you don't have an account, [sign up](https://github.com/join).
2. **Create a New Repository**:
   - Click the **"+"** icon in the top-right corner and select **"New repository"**.
   - Name your repository, e.g., `hello-world-unit-testing`.
   - Add a description (optional).
   - Choose between **Public** or **Private**.
   - Initialize with a **README** (optional).
   - Click **"Create repository"**.

## 3. **Clone the Repository Locally**

Open your terminal or command prompt and execute:

```bash
git clone https://github.com/your-username/hello-world-unit-testing.git
cd hello-world-unit-testing
```

*Replace `your-username` with your actual GitHub username.*

## 4. **Create the "Hello World" Application**

For Python, create a simple script.

1. **Create a Python File**:

   ```bash
   touch hello.py
   ```

2. **Add Code to `hello.py`**:

   ```python
   def say_hello():
       return "Hello, World!"

   if __name__ == "__main__":
       print(say_hello())
   ```

## 5. **Set Up Unit Testing**

Using Python's built-in `unittest` framework.

1. **Create a Tests Directory**:

   ```bash
   mkdir tests
   touch tests/test_hello.py
   ```

2. **Add Unit Tests to `tests/test_hello.py`**:

   ```python
   import unittest
   from hello import say_hello

   class TestHello(unittest.TestCase):
       
       def test_say_hello(self):
           self.assertEqual(say_hello(), "Hello, World!")

   if __name__ == '__main__':
       unittest.main()
   ```

3. **Run Tests Locally**:

   ```bash
   python -m unittest discover tests
   ```

   You should see an output indicating that the tests have passed.

## 6. **Commit and Push Changes to GitHub**

1. **Add Files to Git**:

   ```bash
   git add .
   ```

2. **Commit Changes**:

   ```bash
   git commit -m "Initial commit with Hello World application and unit tests"
   ```

3. **Push to GitHub**:

   ```bash
   git push origin main
   ```

## 7. **Set Up Continuous Integration (CI) with GitHub Actions**

Automate your tests to run on every push.

1. **Create GitHub Actions Workflow**:

   - In your repository on GitHub, navigate to the **"Actions"** tab.
   - Click **"Set up a workflow yourself"** or choose a Python template.
   - Create a file named `.github/workflows/python-app.yml`.

2. **Add the Following Configuration to `python-app.yml`**:

   ```yaml
   name: Python application
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   
   jobs:
     build:
   
       runs-on: ubuntu-latest
   
       steps:
        - name: Checkout code
          uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.x' 
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt || echo "No requirements.txt found"
        - name: Run tests
          run: |
            python -m unittest discover test
   ```

3. **Commit the Workflow File**:

   Commit the new `python-app.yml` to `.github/workflows/`.

4. **Verify CI Runs**:

   - After pushing, go to the **"Actions"** tab to see your workflow running.
   - It should execute the unit tests automatically.

## 8. **Set Up Project Management with Kanban**

GitHub offers built-in project management tools, but you can also use external tools like Trello or Jira. Here, we'll use GitHub Projects.

1. **Navigate to Projects**:

   - In your repository, click on the **"Projects"** tab.
   - Click **"New Project"** and select **"Kanban (Basic)"**.

2. **Configure Columns**:

   - **To Do**: Tasks to be started.
   - **In Progress**: Tasks currently being worked on.
   - **Done**: Completed tasks.

3. **Add Issues as Tasks**:

   - Click **"Add cards"** and create issues representing tasks such as:
     - "Implement `say_hello` function"
     - "Write unit tests for `say_hello`"
     - "Set up GitHub Actions for CI"

4. **Organize and Move Tasks**:

   As you work on tasks, move the corresponding cards across the columns to track progress.

## 9. **Best Practices and Next Steps**

- **Branching Strategy**: Use branches like `feature/say-hello` for new features and merge them into `main` via pull requests after reviews.
- **Code Reviews**: Even for simple projects, practicing code reviews can help maintain quality.
- **Enhance Tests**: Add more unit tests or explore other testing frameworks like `pytest` for more features.
- **Documentation**: Keep your `README.md` updated with project details and instructions.
- **Expand Project**: As you grow more comfortable, expand your project with more functionalities and corresponding tests.

## 10. **Resources and Further Learning**

- **GitHub Guides**:
  - [Hello World](https://guides.github.com/activities/hello-world/)
  - [Setting up CI with GitHub Actions](https://docs.github.com/en/actions/quickstart)
  - [GitHub Projects](https://docs.github.com/en/issues/organizing-your-work-with-projects/learning-about-projects/about-projects)

- **Unit Testing**:
  - [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
  - [pytest Documentation](https://docs.pytest.org/en/7.2.x/)

- **Kanban Methodology**:
  - [Kanban Guide](https://www.atlassian.com/agile/kanban)

- **Version Control**:
  - [Pro Git Book](https://git-scm.com/book/en/v2)

## **Conclusion**

By following these steps, you've set up a basic "Hello World" project with unit testing, integrated it with GitHub for version control, automated testing with GitHub Actions, and organized your workflow using a Kanban board. This foundation can be expanded as you take on more complex projects, incorporating additional best practices and tools as needed.

# AWS GITHUB CICD

Configuring GitHub with AWS involves integrating services from both platforms to facilitate workflows such as continuous integration and continuous deployment (CI/CD). Here's a comprehensive guide to set up GitHub with AWS, focusing on an example of deploying a simple application using AWS services:

### Prerequisites
- A GitHub account.
- An AWS account.
- Basic knowledge of Git and AWS services.

### Steps:

#### 1. **Setting Up Your GitHub Repository**
   - **Create a Repository:** Go to your GitHub account, and create a new repository for your application.
   - **Clone the Repository:** Clone the repository to your local machine using Git for further configuration.

     ```bash
     git clone https://github.com/your-username/your-repo.git
     cd your-repo
     ```
   - **Add Your Code:** Add your application code to this repository and commit the changes.
     ```bash
     git add .
     git commit -m "Initial commit with application code"
     git push origin main
     ```

#### 2. **AWS IAM Role Creation**
   - **Access IAM Console:** Go to the AWS Identity and Access Management (IAM) console.
   - **Create an IAM Role:** 
     - Choose `Roles` and click on `Create role`.
     - Choose `AWS service` and select `EC2` (or any other service like Lambda, depending on deployment).
     - Attach necessary policies to allow access to required AWS resources (e.g., `AmazonS3FullAccess` for S3 or `AmazonEC2FullAccess` for EC2).
     - Name the role and save it.

#### 3. **AWS CodeDeploy Setup**
   - **Access CodeDeploy Console:** Navigate to AWS CodeDeploy service.
   - **Create an Application:**
     - Choose `Create application`.
     - Configure the application with the platform you wish to deploy to (e.g., EC2/On-premises).
   - **Create a Deployment Group:**
     - Specify the EC2 instances (by tags or individually) that should be included in the deployment group.
     - Associate the IAM role created previously.

#### 4. **AWS CodePipeline Setup (Continuous Deployment)**
   - **Access CodePipeline Console:** Go to AWS CodePipeline service.
   - **Create a Pipeline:**
     - Choose `Create pipeline` and provide a name for your pipeline.
     - **Source Stage:**
       - Choose `GitHub` as the source provider.
       - Authenticate with your GitHub account.
       - Select the repository and branch to build and deploy.
     - **Build Stage:**
       - (Optional) Add a build stage using AWS CodeBuild to build your code.
     - **Deploy Stage:**
       - Select `AWS CodeDeploy` as the deployment provider and link it with the application and deployment group created earlier.

#### 5. **Configure GitHub (Access Integration)**
   - **GitHub Webhook (Optional):** Set up a webhook in GitHub to trigger the pipeline on code push events.
     - Go to the GitHub repository, click on `Settings` > `Webhooks`.
     - Add a webhook URL pointing to AWS (CodePipeline can automatically push code updates).

#### 6. **Test the Setup**
   - **Commit Changes:** Push changes to your GitHub repository.
   - **Trigger Pipeline:** Ensure your pipeline is triggered and deploys the changes accordingly.
   - **Monitor Deployment:** Use the AWS CodeDeploy console to check the deployment status and logs.

### Tips
- **Security:** Ensure your AWS access keys and secrets are properly secured.
- **Notifications:** Set up AWS CloudWatch and SNS for deployment success/failure notifications.
- **IAM Policies:** Fine-tune IAM roles and policies to restrict access only to necessary resources.

This integration allows automatic deployments every time code is pushed to the GitHub repository, facilitating a robust CI/CD pipeline.
