import streamlit as st

def get_about_content():
    return """
    **Empowering Medical Billing Advocates with Generative AI.**
    
    MediSync is built for professionals who fight insurance denials every day. We understand that crafting detailed, evidence-based appeal letters is time-consuming and complex.
    
    **Our Mission**
    To democratize access to sophisticated medical reasoning tools, allowing advocates to process claims 10x faster with higher success rates.
    
    **How It Works**
    1.  **Upload**: You provide the denial letter (PDF).
    2.  **Analyze**: Our OCR extracts the text, and our HIPAA-compliant AI engine analyzes the clinical context against standard medical policies.
    3.  **Draft**: We generate a formal appeal letter ready for your review and submission.
    """

def get_addendum_content():
    return """
    This section details the technical lifecycle of Patient Health Information (PHI) within the MediSync platform. It defines how data is ingested, processed, and destroyed to ensure "Zero-Retention" compliance.

    **1. Data Flow Architecture**
    The MediSync system operates on a **Transient Processing Model**. Data submitted by the User is processed in real-time and is not persisted in any permanent database or long-term storage system owned by MediSync.

    **1.1. Ingestion & Transmission**
    * **Transmission:** All file uploads and interactions with the MediSync Platform are transmitted over **HTTPS** using **TLS 1.2+ encryption**.
    * **Upload Buffering:** Upon upload, the Data (PDF Denial Letter) is buffered into the application’s active memory (RAM).

    **1.2. Volatile Processing Pipeline**
    To perform Optical Character Recognition (OCR), the system creates a **transient file instance**. The lifecycle of this instance is strictly bound to the duration of the processing request:
    1.  **Transient Creation:** A temporary, randomly named file is generated in the server's ephemeral storage solely to allow the OCR engine to read the document structure.
    2.  **Extraction:** The OCR engine extracts raw text data from the transient file.
    3.  **Immediate Destruction:** Immediately upon the completion of text extraction, the transient file is **unlinked and deleted** from the file system.

    **1.3. LLM Inference & Third-Party Processing**
    * **Data Minimization:** Only the extracted textual content relevant to the denial is transmitted to the AI Inference Provider (Groq).
    * **Processing:** The inference provider processes the text solely to generate the appeal draft.
    * **No Training:** Data submitted via the API is used strictly for inference and is not used to train the provider's foundation models.

    **1.4. Output & Session State**
    * **In-Memory Result:** The generated appeal draft and extracted context are stored exclusively in **Session State Memory** (RAM) for the duration of the User's active browser session.
    * **Session Termination:** Closing the web browser tab, refreshing the page, or ending the session triggers the immediate clearing of this memory. No copy of the generated appeal is retained on MediSync servers.
    
    <br>
    
    <details>
    <summary><strong>Technical Architecture Reference (Click to Expand)</strong></summary>
    <div style='padding: 10px; border-left: 3px solid #64748b; background: rgba(51, 65, 85, 0.1); margin-top: 10px;'>
    
    *   **Ephemeral Storage Logic**: Utilizes Python `tempfile` library for volatile storage.
    *   **Cleanup Mechanism**: Implements `os.unlink(tmp_path)` for guaranteed file destruction.
    *   **Secrets Management**: Configuration and keys are loaded securely via `.streamlit/secrets.toml`.
    
    </div>
    </details>
    """

def get_compliance_content():
    return """
    **Data Retention Policy**
    MediSync enforces a strict **Zero-Retention Policy** for all Protected Health Information (PHI).

    **2.1. Storage of PHI**
    * **Disk Storage:** MediSync **does not** write PHI to permanent disk storage, databases, or backups.
    * **Databases:** The platform does not maintain a database of patient records, claims history, or appeal logs.
    * **Ephemeral Only:** PHI exists within the MediSync infrastructure only for the milliseconds required to process the OCR and API request.

    **2.2. Logging & Diagnostics**
    * **Sanitized Logs:** System logs capture only operational metrics (e.g., timestamps, success/failure status, error codes, processing duration).
    * **PHI Exclusion:** The content of denial letters, patient names, dates of birth, and diagnosis codes are **explicitly excluded** from all system logs and error traces.
    * **Advocate Profiles:** User-provided "Advocate Profile" data (Name, Title, Address) is stored only in the User's local session or secure environment secrets and is not aggregated by MediSync.

    **2.3. User Responsibility**
    The User acknowledges that because MediSync does not retain data, **no recovery of lost drafts is possible** once the session ends. It is the User's responsibility to download and save generated appeals to their own secure systems immediately upon generation.

    ---

    ### Our Security Promise

    Your denial letters and EOBs often contain sensitive patient information. Our app is designed so that this information is processed securely, never stored, and never reused for any other purpose. All access is tightly controlled and logged to protect your patients and your practice.

    #### Zero‑Retention PHI Processing
    *   **No database of patient records**: The app processes claim documents in encrypted memory to generate appeal drafts, then immediately discards the data.
    *   **Short‑lived processing**: Files and text are held only long enough to create the appeal letter, then are securely wiped from memory.
    *   **PHI‑safe logging**: System logs are designed not to capture patient identifiers, diagnosis codes, or other PHI.

    #### HIPAA‑Aligned Controls
    *   **Encryption in transit and in use**: All data sent between your browser and our service is protected with modern HTTPS/TLS encryption.
    *   **Access control and least privilege**: Only a small, authorized engineering and operations team can access production systems.
    *   **Policies, training, and incident readiness**: We maintain documented security and privacy policies and sign Business Associate Agreements (BAAs).

    #### SOC 2–Oriented Practices
    *   **Structured security program**: We follow standardized controls for access management, change management, and vulnerability management.
    *   **Audit‑ready evidence**: System configurations and access logs are retained as evidence for independent audits.
    """
