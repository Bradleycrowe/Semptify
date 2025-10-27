# Module List for SemptifyAppGUI

## 1. Office Module
- **Functions**:
  - `create_room`: Creates a new room.
  - `list_rooms`: Lists all available rooms.
- **Inputs**:
  - Room Name (Text Box)
  - Room Type (Drop-down: Open, Private)
- **Outputs**:
  - Room creation confirmation.
  - List of rooms.
- **Configuration Options**:
  - Room expiration time (hardcoded to 3600 seconds).

## 2. Document Management Module
- **Functions**:
  - `upload_document`: Initializes document upload.
  - `lock_document`: Locks a document.
  - `annotate_document`: Adds annotations to a document.
- **Inputs**:
  - Document Name (Text Box)
  - Document ID (Text Box)
  - Annotation Text (Text Box)
  - Timecode (Number Input)
- **Outputs**:
  - Upload initialization details.
  - Lock confirmation.
  - Annotation confirmation.
- **Configuration Options**:
  - Document hash (hardcoded as "dummyhash").

## 3. Law Notes Module
- **Functions**:
  - `open_law_notes`: Opens the law notes section in the browser.
- **Inputs**:
  - None.
- **Outputs**:
  - Opens the law notes page in the default browser.
- **Configuration Options**:
  - None.

## 4. Public Exposure Module
- **Functions**:
  - Opens the public exposure page in the browser.
- **Inputs**:
  - None.
- **Outputs**:
  - Opens the public exposure page in the default browser.
- **Configuration Options**:
  - None.

## 5. Enforcement Module
- **Functions**:
  - Opens the enforcement page in the browser.
- **Inputs**:
  - None.
- **Outputs**:
  - Opens the enforcement page in the default browser.
- **Configuration Options**:
  - None.

## 6. General Navigation
- **Functions**:
  - `open_navigation_page`: Opens a specific page in the browser.
- **Inputs**:
  - Endpoint URL (Text Box)
- **Outputs**:
  - Opens the specified page in the default browser.
- **Configuration Options**:
  - None.