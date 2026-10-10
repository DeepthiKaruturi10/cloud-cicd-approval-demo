# Cloud Build CI/CD Pipeline with Approval Gates

A small Flask application and Google Cloud Build configuration demonstrating a CI pipeline plus a separately approval-gated release pipeline.

## Project files

- `app.py` — Flask web app with `/` and `/health` endpoints.
- `test_app.py` — two unit tests.
- `Dockerfile` — container image for Cloud Run.
- `cloudbuild.yaml` — CI: test, build, push image to Artifact Registry.
- `cloudbuild-release.yaml` — release: deploy a previously built image to Cloud Run.
- **The human approval is configured on the release trigger in the Google Cloud Console**, not inside the YAML file.

## A. Run locally (Windows / VS Code)

1. Extract this ZIP.
2. Open the extracted `cloud-cicd-approval-demo` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment and install dependencies:

   Windows PowerShell:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m unittest -v
   python app.py
   ```

   If PowerShell blocks activation, use Command Prompt terminal:
   ```bat
   .venv\Scripts\activate.bat
   ```

5. Open `http://127.0.0.1:8080/` and `http://127.0.0.1:8080/health`.
6. Stop the server with `Ctrl+C`.

## B. Run in Google Cloud Shell Editor

1. Upload/extract this folder into your Cloud Shell home directory, or open Cloud Shell and upload the ZIP.
2. In the terminal:
   ```bash
   cd ~/cloud-cicd-approval-demo
   python3 -m pip install --user -r requirements.txt
   python3 -m unittest -v
   python3 app.py
   ```
3. Use Cloud Shell Web Preview on port `8080` to open the app.

## C. Google Cloud setup (requires permissions and may require active billing)

Cloud deployment is separate from local running. Do not enable paid services or add payment details unless you understand any possible charges.

1. Select the intended project:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```
2. Check billing:
   ```bash
   gcloud billing projects describe YOUR_PROJECT_ID
   ```
   If `billingEnabled` is false, resolve billing or use the local demonstration. Do not assume Google Cloud builds/deployment will work without billing.
3. Enable APIs if permitted:
   ```bash
   gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com
   ```
4. Create the Artifact Registry repository (one-time):
   ```bash
   gcloud artifacts repositories create approval-demo --repository-format=docker --location=asia-south1 --description="Approval demo container images"
   ```
   If it already exists, do not create it again.
5. Ensure the Cloud Build service account has the permissions needed to push to Artifact Registry and deploy to Cloud Run. An administrator may need to configure IAM.
6. Connect the GitHub repository to Cloud Build in the Cloud Build Triggers page.
7. Create the CI trigger:
   - Name: `approval-demo-ci`
   - Event: push to branch `^main$`
   - Config file: `cloudbuild.yaml`
8. Create the release trigger:
   - Name: `approval-demo-release`
   - Choose a release branch/tag or manual trigger strategy.
   - Config file: `cloudbuild-release.yaml`
   - Enable **Require approval** on the trigger.
   - Set `_IMAGE_TAG` to the actual short commit SHA for an image that was successfully pushed by CI.
9. A release build should wait for an authorized approver. Approve it in Cloud Build History. After it succeeds, open Cloud Run and the `approval-demo` service URL.

## Important notes

- The CI configuration builds and pushes the image tagged with `$SHORT_SHA`.
- The release configuration must deploy the exact image tag created by CI. Replace `_IMAGE_TAG` with the actual short SHA from the CI build; do not leave `REPLACE_WITH_CI_SHORT_SHA`.
- Approval is a Cloud Build trigger setting and requires the approver to have the appropriate IAM role (Cloud Build Approver).
- A working cloud deployment depends on billing status, APIs, IAM permissions, repository connection, and trigger configuration.
- Never commit passwords, access tokens, service-account keys, or `.env` secrets.
