# README_VERIFY.md

# Verification Module

## Installation Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd semptify-verify-module
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the environment variables by copying the example configuration:
   ```
   cp modules/verify/config.example.env .env
   ```

4. Edit the `.env` file to configure the necessary environment variables.

## Configuration Details

The following environment variables are required for the verification module:

- `VERIFY_ENDPOINT`: URL to pull the library manifest.
- `VERIFY_API_KEY`: (Optional) Secure authentication header for the API.
- `VERIFY_POLL_INTERVAL`: Default is 300 seconds; can be overridden in the GUI.
- `VERIFY_MAX_RETRIES`: Default is 5 retries for transient errors.
- `VERIFY_LOG_PATH`: Path for persistent logs.

## Expected Outputs

Upon successful execution, the module will:

- Fetch the library manifest from the specified `VERIFY_ENDPOINT`.
- Validate the manifest against the defined schema in `verify_schema.json`.
- Download artifacts, compute their SHA256 hashes, and compare them to the manifest.
- Log the results and update the GUI status.
- Provide a checkpoint JSON file in the specified log path.

## Recovery Steps

In case of errors or failures during the verification process:

1. Check the logs located in the `logs` directory for detailed error messages.
2. Review the checkpoint files in `logs/checkpoints` for the last successful run.
3. If an artifact is marked as quarantined, follow the rollback suggestion provided in the GUI.
4. Ensure that the environment variables are correctly set and that the `VERIFY_ENDPOINT` is reachable.

## Additional Notes

- For testing, a sample manifest is provided in `demo_manifest.json`.
- To run the verification module, access the GUI at `modules/verify/templates/verify/verify_module.html` and use the "Re-verify Now" button.
- Ensure that the development server is running before executing tests or using the GUI.
