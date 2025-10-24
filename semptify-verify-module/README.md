# Semptify Verification Module

## Overview
The Semptify Verification Module is designed to fetch, validate, and manage library manifests from a specified endpoint. It ensures the integrity of artifacts by computing SHA256 hashes and provides a user-friendly interface for monitoring the verification process.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd semptify-verify-module
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables. You can use the provided `.env.example` and `modules/verify/config.example.env` as templates.

## Configuration
- **VERIFY_ENDPOINT**: URL to pull the library manifest.
- **VERIFY_API_KEY**: (Optional) Secure authentication header for the API.
- **VERIFY_POLL_INTERVAL**: Default is 300 seconds; can be overridden in the GUI.
- **VERIFY_MAX_RETRIES**: Default is 5 retries for transient errors.
- **VERIFY_LOG_PATH**: Path for persistent logs.

## Usage
1. Start the development server:
   ```
   python -m flask run
   ```

2. Access the verification module through the web interface at `/modules/verify`.

3. Use the "Re-verify Now" button to manually trigger a verification process.

## Expected Outputs
- The module will log the status of each verification run, including success, failures, and any artifacts that are quarantined due to hash mismatches.
- Checkpoint JSON files will be created in the `logs/checkpoints` directory for recovery and auditing purposes.

## Recovery Steps
In case of failures:
- Review the logs located in the specified `VERIFY_LOG_PATH`.
- Check the checkpoint files for the last successful verification state.
- Use the quarantine feature to roll back any mismatched artifacts.

## Additional Information
For detailed information on the module's functionality, refer to the following files:
- `modules/verify/README_VERIFY.md`: Specific instructions for the verification module.
- `modules/verify/tests/verify_tests.py`: Unit tests covering various scenarios.

This module is a crucial part of the Semptify project, ensuring that all library artifacts are verified and secure.
