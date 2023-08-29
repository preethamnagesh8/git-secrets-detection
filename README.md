# Git Secrets Detection
Welcome to the Git Secrets Detection repository! Git Secrets Detection is a tool that helps developers detect and secure secrets in their source code. Secrets, such as passwords and API keys, are often used to authenticate or authorize access to systems, services, or resources, and are critical to the security of an application. However, if these secrets are accidentally or maliciously exposed in a codebase, they can be easily accessed by attackers and used to compromise systems, steal data, and disrupt operations.

Git Secrets Detection helps developers identify and secure secrets in their codebases, reducing the risk of unauthorized access and data breaches. It uses static analysis techniques, to scan codebases for secrets, alerting developers to any secrets that are detected.

By using Git Secrets Detection, developers can protect their systems and data, maintain compliance with regulatory requirements, and build trust with users and stakeholders. Whether you are developing a small application or a large, complex system, Git Secrets Detection can help you secure your secrets and ensure the security and integrity of your codebase.

## Getting Started
To get started with this project, you will need to clone the repository and install the required dependencies. You can do this by running the following commands:

```
git clone https://github.com/preethamnagesh8/git-secrets-detection
cd git-secrets-detection
pip install -r requirements.txt
```

Once the dependencies are installed, you can start the application by running the following command:

```
python manage.py runserver
```


This will start the Git Secrets Detection security system, which you can access through your web browser at http://localhost:8000

## Features
- Detect 20 different types of secrets in git repositories
- Scan every historic commit to ensure no secrets are hidden in code base
- Verify identified secrets to see if secrets are actively being used

## Contributing
We welcome contributions to this project! If you would like to contribute, please follow these guidelines:
- Create a new branch for your changes
- Make your changes, including tests if applicable
- Submit a pull request for review

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [Preetham Nagesh](https://www.linkedin.com/in/preetham-nagesh/).

