import streamlit as st
import pandas as pd
from groq import Groq

# Setup API key for Groqcloud
api_key = st.secrets["api_key"]
client = Groq(api_key=api_key)

# Define the optimized and detailed prompt templates
preprocess_prompt_template = """
A user wants to create documentation for software development (website, app, etc.).
You are an AI assistant specializing in pre-processing data.
Analyze the given data and provide a detailed summary.
Identify key information and functional requirements for the software from the processed data.
Ensure the summary includes a clear explanation of each identified item and its importance.
Describe all the functions required to build the complete software

### Example Format:
- **Key Information**:
  - [Description of key information]
- **Functional Requirements**:
  - [Description of functional requirements]
"""

brd_prompt_template = """
A user wants to create documentation for software development (website, app, etc.).
You are an AI assistant specialized in generating Business Requirement Documents (BRD). Use the provided data summary to create a detailed BRD. Follow the structure and provide clear, concise information. Ensure each section is comprehensive and includes relevant details.

### Business Requirement Document
- **Title:** [Project Title]
- **Overview** [Brief overview of the project]
- **Project Scope:** [Description of project scope]
- **Business Requirements:**
  1. [Business requirement 1]
  2. [Business requirement 2]
- **Non-Functional Requirements:**
  1. [Non-functional requirement 1]
  2. [Non-functional requirement 2]
"""

frd_prompt_template = """
A user wants to create documentation for software development (website, app, etc.).
You are an AI assistant specialized in generating Functional Requirement Documents (FRD). Use the provided BRD to create a detailed FRD. Follow the structure and provide clear, detailed descriptions. Ensure each section is comprehensive and includes relevant technical details.

### Functional Requirement Document
- **Title:** [Module Title]
- **Overview:** [Brief overview of the module]
- **Detailed Functional Description:**
  1. [Functional requirement 1]
  2. [Functional requirement 2]
"""

use_case_prompt_template = """
A user wants to create documentation for software development (website, app, etc.).
You are an AI assistant specialized in generating Use Case Documentation. Use the provided FRD to create detailed use case documentation. Follow the structure and provide comprehensive descriptions. Provide a comprehensive list of all relevant use cases derived from the provided FRD.

### Example Format

**I. Use Case 1** 
- **Use Case Name:** [Name of the use case]
- **Actors:** [List of actors]
- **Preconditions:** [Conditions that must be met before the use case starts]
- **Postconditions:** [Conditions that must be met after the use case ends]
- **Main Flow:**
  1. [Step 1]
  2. [Step 2]
- **Alternate Flows:**
  1. [Alternative step 1]
  2. [Alternative step 2]
- **Triggers:** [What triggers the use case]
- **Assumptions:** [Assumptions made for the use case]
- **Detailed Description:** [Detailed description of the use case]
- **Notes:** [Additional notes]

**II. Use Case 2** 
- **Use Case Name:** [Name of the use case]
- **Actors:** [List of actors]
- **Preconditions:** [Conditions that must be met before the use case starts]
- **Postconditions:** [Conditions that must be met after the use case ends]
- **Main Flow:**
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- **Alternate Flows:**
  1. [Alternative step 1]
  2. [Alternative step 2]
  3. [Alternative step 3]
- **Triggers:** [What triggers the use case]
- **Assumptions:** [Assumptions made for the use case]
- **Detailed Description:** [Detailed description of the use case]
- **Notes:** [Additional notes]
"""

data_modeling_prompt_template = """
A user wants to create documentation for software development (website, app, etc.).
You are an AI assistant specialized in generating Data Models. Use the provided FRD and Use Case Documentation to create detailed data models (ERD, Logical Data Model).

### Data Models
- **Entity-Relationship Diagram (ERD):** [Description]
- **Logical Data Model:** [Description]
"""

wireframes_mockups_prompt_template = """
A user wants to create documentation for software development (website, app, etc.).
You are an AI assistant specialized in generating Wireframes and Mockups. Use the provided FRD and Use Case Documentation to create detailed wireframes and mockups.

### Wireframes and Mockups
- **Basic Wireframes:** [Description and diagrams]
- **Detailed Mockups:** [For each screen, provide a detailed list of components]
"""

# sdd_prompt_template = """
# A user wants to create documentation for software development (website, app, etc.).
# You are an AI assistant specialized in generating System Design Documents (SDD). Use the provided FRD, Use Case Documentation, Data Models, and Wireframes and Mockups to create a detailed SDD.

# ### System Design Document
# - **System Architecture:** [Description and design]
# - **Database Design:** [Description and design]
# - **User Interface Design:** [Description and design]
# - **Class Diagram:** [Description and diagram]
# - **Activity Diagram:** [Description and diagram]
# - **Sequence Diagram:** [Description and diagram]
# """

def call_llm_api(prompt_template, user_content):
    data = {
        "model": "llama3-groq-70b-8192-tool-use-preview",
        "messages": [
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": user_content}
        ]
    }
    response = client.chat.completions.create(**data)
    return response.choices[0].message.content

# Streamlit interface
st.title("Business Analysis Assistant")

# Initialize session state variables
if 'data_summary' not in st.session_state:
    st.session_state['data_summary'] = None
if 'important_info' not in st.session_state:
    st.session_state['important_info'] = None
if 'functional_requirements' not in st.session_state:
    st.session_state['functional_requirements'] = None
if 'brd' not in st.session_state:
    st.session_state['brd'] = None
if 'frd' not in st.session_state:
    st.session_state['frd'] = None
if 'use_case_doc' not in st.session_state:
    st.session_state['use_case_doc'] = None
if 'data_modeling' not in st.session_state:
    st.session_state['data_modeling'] = None
if 'wireframes_mockups' not in st.session_state:
    st.session_state['wireframes_mockups'] = None
if 'sdd' not in st.session_state:
    st.session_state['sdd'] = None

# Step 1: Data Preprocessing
def data_preprocessing():
    st.header('Step 1: Data Preprocessing')

    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Excel Data:", df)

        if st.button('Process Data'):
            with st.spinner("Processing..."):
                analysis_prompt = f"Analysis this data:\n{df.to_string()}"
                data_summary = call_llm_api(preprocess_prompt_template, analysis_prompt)

                # Extract key information and functional requirements
                st.session_state['data_summary'] = data_summary

                # Extract important information and functional requirements
                if "Functional Requirements:" in data_summary:
                    parts = data_summary.split("Functional Requirements:")
                    important_info = parts[0].strip()
                    functional_requirements = parts[1].strip()
                else:
                    important_info = data_summary.strip()
                    functional_requirements = ""

                st.session_state['important_info'] = important_info
                st.session_state['functional_requirements'] = functional_requirements

            st.write("### Data Summary:")
            st.write(st.session_state['data_summary'])

            return st.session_state['data_summary']

# Step 2: Business Requirement Documents
def business_requirement_documents():
    st.header('Step 2: Business Requirement Documents')

    if st.session_state['data_summary']:
        st.write("### Data Summary from Step 1:")
        st.write(st.session_state['data_summary'])

    if st.button('Generate BRD'):
        with st.spinner("Generating BRD..."):
            gen_brd_prompt = f"Generata BRD from this summary:\n{st.session_state['data_summary']}"
            st.session_state['brd'] = call_llm_api(brd_prompt_template, gen_brd_prompt)

        st.write("### Generated Business Requirement Document:")
        st.write(st.session_state['brd'])

        return st.session_state['brd']

# Step 3: Functional Requirement Documents
def functional_requirement_document():
    st.header('Step 3: Functional Requirement Documents')

    if st.session_state['brd']:
        st.write("### Business Requirement Documents from Step 2:")
        st.write(st.session_state['brd'])

    if st.button('Generate FRD'):
        with st.spinner("Generating FRD..."):
            gen_frd_prompt = f"""
            Generata FRD from following BRD and Functional Requirements:
            - Business Requirement Documents: {st.session_state['brd']}
            - Functional Requirements: {st.session_state['functional_requirements']}
            """
            st.session_state['frd'] = call_llm_api(frd_prompt_template, gen_frd_prompt)

        st.write("### Generated Functional Requirement Documents:")
        st.write(st.session_state['frd'])

        return st.session_state['frd']

# Step 4: Use Case Documentation
def use_case_documentation():
    st.header('Step 4: Use Case Documentation')

    if st.session_state['frd']:
        st.write("### Functional Requirement Documents from Step 3:")
        st.write(st.session_state['frd'])

    if st.button('Generate Use Case Document'):
        with st.spinner("Generating Use Case Document..."):
            gen_use_case_prompt = f"""
            Generata Use Case Document from following BRD and FRD:
            - Business Requirement Documents: {st.session_state['brd']}
            - Functional Requirement Documents: {st.session_state['frd']}
            """
            st.session_state['use_case_doc'] = call_llm_api(use_case_prompt_template, gen_use_case_prompt)

        st.write("### Generated Use Case Document:")
        st.write(st.session_state['use_case_doc'])

        return st.session_state['use_case_doc']

# Step 5: Data Modeling
def data_modeling():
    st.header('Step 5: Data Modeling')

    if st.session_state['frd'] and st.session_state['use_case_doc']:
        st.write("### Functional Requirement Documents from Step 3:")
        st.write(st.session_state['frd'])
        st.write("### Use Case Documentation from Step 4:")
        st.write(st.session_state['use_case_doc'])

    if st.button('Generate Data Modeling'):
        with st.spinner("Generating Data Modeling..."):
            gen_data_modeling_prompt = f"""
            Generate Data Models from following FRD and Use Case Documentation:
            - Functional Requirement Documents: {st.session_state['frd']}
            - Use Case Documentation: {st.session_state['use_case_doc']}
            """
            st.session_state['data_modeling'] = call_llm_api(data_modeling_prompt_template, gen_data_modeling_prompt)

        st.write("### Generated Data Modeling:")
        st.write(st.session_state['data_modeling'])

        return st.session_state['data_modeling']

# Step 6: Wireframes and Mockups
def wireframes_and_mockups():
    st.header('Step 6: Wireframes and Mockups')

    if st.session_state['frd'] and st.session_state['use_case_doc']:
        st.write("### Functional Requirement Documents from Step 3:")
        st.write(st.session_state['frd'])
        st.write("### Use Case Documentation from Step 4:")
        st.write(st.session_state['use_case_doc'])

    if st.button('Generate Wireframes and Mockups'):
        with st.spinner("Generating Wireframes and Mockups..."):
            gen_wireframes_mockups_prompt = f"""
            Generate Wireframes and Mockups from following FRD and Use Case Documentation:
            - Functional Requirement Documents: {st.session_state['frd']}
            - Use Case Documentation: {st.session_state['use_case_doc']}
            """
            st.session_state['wireframes_mockups'] = call_llm_api(wireframes_mockups_prompt_template, gen_wireframes_mockups_prompt)

        st.write("### Generated Wireframes and Mockups:")
        st.write(st.session_state['wireframes_mockups'])

        return st.session_state['wireframes_mockups']

# Step 7: System Design Document (SDD)
# def system_design_document():
#     st.header('Step 7: System Design Document (SDD)')

#     if st.session_state['frd'] and st.session_state['use_case_doc'] and st.session_state['data_modeling'] and st.session_state['wireframes_mockups']:
#         st.write("### Functional Requirement Documents from Step 3:")
#         st.write(st.session_state['frd'])
#         st.write("### Use Case Documentation from Step 4:")
#         st.write(st.session_state['use_case_doc'])
#         st.write("### Data Modeling from Step 5:")
#         st.write(st.session_state['data_modeling'])
#         st.write("### Wireframes and Mockups from Step 6:")
#         st.write(st.session_state['wireframes_mockups'])

#     if st.button('Generate System Design Document'):
#         with st.spinner("Generating System Design Document..."):
#             gen_sdd_prompt = f"""
#             Generate System Design Document from following documents:
#             - Functional Requirement Documents: {st.session_state['frd']}
#             - Use Case Documentation: {st.session_state['use_case_doc']}
#             - Data Modeling: {st.session_state['data_modeling']}
#             - Wireframes and Mockups: {st.session_state['wireframes_mockups']}
#             """
#             st.session_state['sdd'] = call_llm_api(sdd_prompt_template, gen_sdd_prompt)

#         st.write("### Generated System Design Document:")
#         st.write(st.session_state['sdd'])

#         return st.session_state['sdd']

# Main function to integrate all steps
def main():
    st.sidebar.title("Business Analyst Assistant")
    step = st.sidebar.radio("Select Step", ["Step 1: Data Preprocessing", "Step 2: Business Requirement Documents", 
                                            "Step 3: Functional Requirement Document", "Step 4: Use Case Documentation", 
                                            "Step 5: Data Modeling", "Step 6: Wireframes and Mockups"])

    if step == "Step 1: Data Preprocessing":
        data_summary = data_preprocessing()
    elif step == "Step 2: Business Requirement Documents":
        if st.session_state['data_summary'] is None:
            st.warning("Please complete Step 1: Data Preprocessing first.")
        else:
            brd = business_requirement_documents()
    elif step == "Step 3: Functional Requirement Document":
        if st.session_state['brd'] is None:
            st.warning("Please complete Step 2: Business Requirement Documents first.")
        else:
            frd = functional_requirement_document()
    elif step == "Step 4: Use Case Documentation":
        if st.session_state['frd'] is None:
            st.warning("Please complete Step 3: Functional Requirement Document first.")
        else:
            use_case_documentation()
    elif step == "Step 5: Data Modeling":
        if st.session_state['frd'] is None or st.session_state['use_case_doc'] is None:
            st.warning("Please complete Step 3: Functional Requirement Document and Step 4: Use Case Documentation first.")
        else:
            data_modeling()
    elif step == "Step 6: Wireframes and Mockups":
        if st.session_state['frd'] is None or st.session_state['use_case_doc'] is None:
            st.warning("Please complete Step 3: Functional Requirement Document and Step 4: Use Case Documentation first.")
        else:
            wireframes_and_mockups()
    # elif step == "Step 7: System Design Document":
    #     if st.session_state['frd'] is None or st.session_state['use_case_doc'] is None or st.session_state['data_modeling'] is None or st.session_state['wireframes_mockups'] is None:
    #         st.warning("Please complete Step 3: Functional Requirement Document, Step 4: Use Case Documentation, Step 5: Data Modeling and Step 6: Wireframes and Mockups first.")
    #     else:
    #         system_design_document()

if __name__ == '__main__':
    main()
