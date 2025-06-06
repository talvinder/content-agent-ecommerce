## Product Requirements Document: E-commerce Content-Agent Bot (Workshop Edition)

**1. Introduction & Goals**

*   **Product Name:** E-commerce Content-Agent Bot (Workshop Edition)
*   **Version:** 1.0 (for 91mobiles AI-Powered Product Growth Accelerator)
*   **Project Goal:** To provide workshop participants with a hands-on, Dockerized Python application that demonstrates how Large Language Models (LLMs) can be leveraged as "agents" to generate diverse, persona-driven e-commerce content from structured product data.
*   **Primary Learning Objectives for Participants:**
    *   Understand prompt engineering fundamentals for content generation.
    *   Learn to interact with LLM APIs programmatically.
    *   See how to structure a simple AI agent for a specific task.
    *   Gain experience with Docker for packaging and running AI applications.
    *   Appreciate the role of structured data and persona in guiding AI output.
*   **Target Users:** Participants of the 91mobiles workshop (Product Leads, UX Leads, Tech Leads).

**2. Functional Requirements (FR)**

| ID  | Requirement Description                                                                                                                              | Priority | Notes                                                                                                                                                                                                                                      |
| :-- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR1 | The system MUST accept structured product data as input, specifically in JSON format.                                                              | Must-have  | A sample `sample_product.json` file will be provided. The structure should be clearly defined.                                                                                                                                       |
| FR2 | The system MUST allow users to specify a content generation task via a named prompt template.                                                        | Must-have  | E.g., "generate product description," "generate SEO snippets." Templates will be stored as text files.                                                                                                                                       |
| FR3 | The system MUST interact with a configured Large Language Model (LLM) API (e.g., OpenAI's GPT series) to generate content based on the input and prompt. | Must-have  | API key management will be via a `config.py` file.                                                                                                                                                                                         |
| FR4 | The system MUST output the generated content in a human-readable format (e.g., plain text or Markdown) to the console.                               | Must-have  |                                                                                                                                                                                                                                            |
| FR5 | The system MUST be packaged as a Docker container for easy setup and execution using Docker Compose.                                                 | Must-have  | Ensures consistent environment across participants.                                                                                                                                                                                        |
| FR6 | The system SHOULD allow for easy modification and addition of prompt templates without code changes (i.e., by editing/adding text files).            | Should-have| Facilitates experimentation during the workshop.                                                                                                                                                                                           |
| FR7 | The system SHOULD provide clear feedback to the user regarding its operations (e.g., "Loading product data...", "Generating content using template X..."). | Should-have| Enhances user experience and understanding.                                                                                                                                                                                              |
| FR8 | The system COULD allow users to pass a "persona" string or reference a persona file to influence the tone/style of the generated content.              | Could-have | If time permits. Could be integrated into the prompt template or as a separate parameter. For v1.0, persona can be embedded within the prompt template itself for simplicity.                                                             |
| FR9 | The system COULD output generated content to a specified file instead of/in addition to the console.                                                 | Could-have | Useful for saving outputs.                                                                                                                                                                                                                   |

**3. Non-Functional Requirements (NFR)**

| ID   | Requirement Description                                                                                                         | Priority | Notes                                                                                                                                                                                                        |
| :--- | :------------------------------------------------------------------------------------------------------------------------------ | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NFR1 | **Usability:** The application MUST be runnable via a single, simple command (e.g., `docker-compose run ...` or `python app/main.py ...`). | Must-have  | Clear CLI arguments.                                                                                                                                                                                           |
| NFR2 | **Reliability:** The core functionality (content generation for valid inputs) MUST work reliably. Basic error handling for common issues (e.g., missing API key, file not found) should be present. | Must-have  | Not aiming for production-grade robustness, but should handle workshop scenarios.                                                                                                                            |
| NFR3 | **Maintainability/Extensibility (for workshop):** The code SHOULD be well-structured and commented to allow participants to understand and potentially modify it. | Should-have| Focus on clarity over premature optimization.                                                                                                                                                                    |
| NFR4 | **Performance:** For workshop purposes, content generation for a single product SHOULD complete within a reasonable timeframe (e.g., < 30 seconds), dependent on LLM API response times. | Should-have| Not a high-performance system, but shouldn't feel sluggish.                                                                                                                                                    |
| NFR5 | **Security:** API keys MUST NOT be hardcoded in the application. They will be managed via an external `config.py` file (which is gitignored). | Must-have  | Standard practice.                                                                                                                                                                                           |
| NFR6 | **Offline First (for Docker build):** The Docker image build should be self-contained as much as possible once base images and Python packages are downloaded. | Should-have| Good for workshop environments with potential internet issues after initial setup.                                                                                                                               |

**4. System Architecture & Design (High-Level)**

*   **Language:** Python (version 3.9 or higher)
*   **Orchestration:** Command-Line Interface (CLI) application.
*   **Core Components:**
    1.  **Input Handler:** Loads and validates product data (JSON) and prompt templates (text files).
    2.  **Prompt Constructor:** Combines product data with the selected prompt template to create the final prompt for the LLM.
    3.  **LLM Interaction Module (`agent.py`):**
        *   Manages API key configuration.
        *   Sends requests to the LLM API.
        *   Handles API responses and extracts the generated content.
    4.  **Output Handler:** Prints generated content to the console (or file, if FR9 is implemented).
*   **Deployment:** Docker container managed by Docker Compose.

**5. Data Model**

*   **Input Product Data (`sample_product.json`):**
    *   A JSON file containing a list of product objects or a single product object.
    *   Each product object should have well-defined fields. Example fields for a mobile phone:
        ```json
        {
          "id": "SKU123",
          "name": "Galaxy Stellaris Pro",
          "brand": "Samsung",
          "price_inr": 69999,
          "display": {
            "type": "Dynamic AMOLED 2X",
            "size_inches": 6.7,
            "resolution": "3088 x 1440"
          },
          "camera": {
            "rear_primary_mp": 108,
            "rear_secondary_mp": [12, 10, 10],
            "front_mp": 40
          },
          "processor": "Snapdragon 8 Gen X",
          "ram_gb": 12,
          "storage_gb": 256,
          "battery_mah": 5000,
          "key_features": [
            "Advanced Nightography Camera",
            "120Hz Adaptive Refresh Rate Display",
            "S-Pen Support (Optional)",
            "5G Connectivity"
          ],
          "brief_description": "Experience the next level of mobile technology with the Galaxy Stellaris Pro, featuring a pro-grade camera system and a stunning dynamic display."
        }
        ```
    *   **Note:** The PRD should define a *minimum viable set* of fields. The workshop can discuss adding more.
*   **Prompt Templates (`templates/*.txt`):**
    *   Plain text files.
    *   Use placeholders (e.g., `{product_name}`, `{product_brand}`, `{product_key_features}`) that will be replaced by actual product data.
    *   Example `description_prompt.txt`:
        ```
        You are an expert e-commerce copywriter for 91mobiles, specializing in mobile phones. Your tone is informative, enthusiastic, and slightly tech-savvy, aimed at users looking to make informed purchase decisions.

        Generate a compelling and engaging product description of approximately 150-200 words for the following mobile phone. Highlight its key selling points and unique features. Avoid excessive jargon unless it's a key differentiator.

        Mobile Phone Details:
        Name: {name}
        Brand: {brand}
        Price (INR): {price_inr}
        Display Type: {display_type}
        Display Size: {display_size_inches} inches
        Primary Camera: {camera_rear_primary_mp} MP
        Processor: {processor}
        RAM: {ram_gb} GB
        Storage: {storage_gb} GB
        Key Features: {key_features_list_str}
        Brief Existing Description: {brief_description}

        Generated Product Description:
        ```
*   **Configuration (`config.py`):**
    *   Stores API keys. Example: `OPENAI_API_KEY = "sk-..."`

**6. Technical Specifications & Logic Flow**

*   **`main.py` (CLI Orchestrator):**
    1.  **Argument Parsing (`argparse`):**
        *   `--product_file` (str, required): Path to the input product JSON file.
        *   `--template_name` (str, required): Name of the prompt template file (e.g., `description_prompt` - the `.txt` can be appended internally).
        *   `--output_file` (str, optional): Path to save the output.
    2.  **Load Product Data:**
        *   Read the JSON file specified by `--product_file`.
        *   Handle potential file not found or JSON parsing errors.
        *   If the JSON contains a list, process each product (or just the first for simplicity in v1.0).
    3.  **Load Prompt Template:**
        *   Construct the template file path (e.g., `app/templates/{template_name}.txt`).
        *   Read the content of the template file.
        *   Handle potential file not found errors.
    4.  **Instantiate and Use Agent (`agent.py`):**
        *   Create an instance of the `ContentAgent`.
        *   Call a method like `agent.generate_content(product_data_dict, prompt_template_string)`.
    5.  **Output Handling:**
        *   Print the generated content to the console.
        *   If `--output_file` is provided, write the content to this file.

*   **`agent.py` (ContentAgent Class):**
    1.  **Constructor `__init__(self, api_key)`:**
        *   Store the API key.
        *   Initialize the LLM client (e.g., `openai.OpenAI(api_key=api_key)`).
    2.  **Method `_construct_prompt(self, product_data: dict, prompt_template: str) -> str`:**
        *   This is the core of prompt engineering.
        *   Iterate through placeholders in `prompt_template` (e.g., `{name}`, `{display_type}`).
        *   Access corresponding values from `product_data` dictionary.
            *   Need to handle nested keys (e.g., `product_data['display']['type']` for `{display_type}`). A helper function to flatten or access nested keys might be useful.
            *   For list values like `key_features`, convert them to a comma-separated string or a bulleted list string for insertion into the prompt (e.g., `key_features_list_str`).
        *   Replace placeholders with actual data.
        *   Return the fully constructed prompt string.
    3.  **Method `generate_content(self, product_data: dict, prompt_template: str, llm_model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 500) -> str`:**
        *   Call `_construct_prompt` to get the final prompt.
        *   Make the API call to the LLM:
            ```python
            # Example for OpenAI
            response = self.client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful e-commerce content generation assistant."}, # System prompt can also be part of the main template
                    {"role": "user", "content": final_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            generated_text = response.choices[0].message.content.strip()
            ```
        *   Handle potential API errors (e.g., rate limits, authentication errors) gracefully.
        *   Return the extracted `generated_text`.

*   **`config.py`:**
    *   `OPENAI_API_KEY = "YOUR_API_KEY_HERE"` (This file should be in `.gitignore`).
    *   The application should try to import `OPENAI_API_KEY` from `config`. If `config.py` or the key is missing, it should print an informative error and exit.

*   **`Dockerfile`:**
    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /usr/src/app
    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    # CMD ["python", "app/main.py", "--product_file", "data/sample_product.json", "--template_name", "description_prompt"] 
    # CMD is optional if using docker-compose to specify command
    ```

*   **`docker-compose.yml`:**
    ```yaml
    version: '3.8'
    services:
      content_agent:
        build: .
        volumes:
          - ./app:/usr/src/app/app
          - ./data:/usr/src/app/data
          - ./config.py:/usr/src/app/config.py # Mount config for easy key changes
        # command: python app/main.py --product_file data/sample_product.json --template_name description_prompt
        # Environment variables can also be used for API keys if preferred over config.py mounting
        # environment:
        #   - OPENAI_API_KEY=${OPENAI_API_KEY_FROM_HOST_ENV} 
    ```
    *   The `command` in `docker-compose.yml` allows users to easily change input files/templates without rebuilding the image, by just editing the compose file or overriding the command. Alternatively, make the `CMD` in Dockerfile more generic or expect users to pass the command directly: `docker-compose run content_agent python app/main.py ...`

**7. Error Handling & Edge Cases (Examples)**

*   `config.py` not found or API key missing.
*   Product JSON file not found or invalid JSON.
*   Prompt template file not found.
*   LLM API errors (authentication, rate limits, server errors).
*   Placeholders in template not found in product data (log a warning, continue with empty string or placeholder text).

**8. Future Considerations (Beyond Workshop v1.0 - Good to mention)**

*   Support for multiple LLM providers.
*   More sophisticated agentic behavior (e.g., multi-step prompts, tool use).
*   Web interface (e.g., using Flask/Streamlit).
*   Batch processing of multiple products.
*   Integration with a proper database for products.

**9. README.md (As per your previous excellent outline)**

*   Ensure it clearly states how to set up `config.py`.
*   Give explicit `docker-compose run content_agent python app/main.py --product_file data/sample_product.json --template_name description_prompt` examples.

---

This PRD provides a solid blueprint. The "Authoritative" aspect comes from:
*   Clear, structured requirements.
*   Well-defined architecture using standard tools (Python, Docker).
*   Emphasis on best practices (config management for API keys, clear CLI).
*   Consideration of usability and learning objectives for the workshop participants.
*   A clear path from a simple concept to a working (albeit basic) AI application.

When your coding agent implements this, focusing on the "Must-have" and "Should-have" requirements first will ensure a functional core for the workshop. The logic flow for `agent.py` and `main.py` is the heart of the application.