## Setup

### 1. Create an IAM User

Create an IAM user in AWS and attach the following permission:

```text
AmazonBedrockFullAccess
```

After creating the user, go to **Security credentials → Create access key**.

For the access key use case, select:
<img width="350" alt="AWS access key use case" src="https://github.com/user-attachments/assets/0b0963ba-8565-4517-87e7-d8639803ac1d" />



```text
Application running outside AWS
```

Save the generated **Access Key ID** and **Secret Access Key** securely.


---

### 2. Create a Virtual Environment

Create a Conda environment inside the project folder:

```bash
conda create -p venv python=3.11 -y
```

Activate the environment:

```bash
conda activate .\venv
```

---

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

### 4. Configure AWS Credentials

Configure the AWS CLI using the credentials generated for your IAM user:

```bash
aws configure
```

Enter the following when prompted:

```text
AWS Access Key ID: <your-access-key-id>
AWS Secret Access Key: <your-secret-access-key>
Default region name: us-east-1
Default output format: json
```

---

### 5. Verify AWS Configuration

Check whether your AWS credentials are configured correctly:

```bash
aws sts get-caller-identity
```

If the command returns your AWS account and IAM user details, the configuration is ready.

---

### 6. Run the Application

Once the environment and AWS credentials are configured, run the application using the project's start command(for running streamlit application).
```bash
streamlit run app.py
```
