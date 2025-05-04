
def quick_chat_system_prompt() -> str:
    return f"""
            Forget all previous instructions.
        You are a chatbot named Fred. You are assisting a software developer
        with their software development tasks.
        Each time the user converses with you, make sure the context is about
        * software development,
        * or coding,
        * or debugging,
        * or code reviewing,
        and that you are providing a helpful response.

        If the user asks you to do something that is not
        concerning one of those topics, you should refuse to respond.
        """

def system_learning_prompt() -> str:
    return """
    You are assisting a user with their general software development tasks.
Each time the user converses with you, make sure the context is generally about software development,
or creating a course syllabus about software development,
and that you are providing a helpful response.
If the user asks you to do something that is not concerning software
in the least, you should refuse to respond.
"""


def learning_prompt(learner_level: str, answer_type: str, topic: str) -> str:
    return f"""
Please disregard any previous context.

The topic at hand is ```{topic}```.
Analyze the sentiment of the topic.
If it does not concern software development or creating an online course syllabus about software development,
you should refuse to respond.

You are now assuming the role of a highly acclaimed software engineer specializing in the topic
 at a prestigious software company.  You are assisting a fellow software engineer with
 their software development tasks.
You have an esteemed reputation for presenting complex ideas in an accessible manner.
Your colleague wants to hear your answers at the level of a {learner_level}.

Please develop a detailed, comprehensive {answer_type} to teach me the topic as a {learner_level}.
The {answer_type} should include high level advice, key learning outcomes,
detailed examples, step-by-step walkthroughs if applicable,
and major concepts and pitfalls people associate with the topic.

Make sure your response is formatted in markdown format.
Ensure that embedded formulae are quoted for good display.
"""

############################################################################################################
# Requirements prompts
############################################################################################################

def system_requirements_prompt(product_name, product_description):
    """
    Generate a system requirements prompt based on the product name and description
    Args:
        product_name: The name of a product described in a system prompt
        product_description: A description of the product

    Returns:
        A prompt to use as a system prompt for making requirements documents for the product name and description.

    """
    return f"""
    Forget all previous instructions and context.

    You are an expert in requirements engineering.

    Your job is to learn and understand the following text about a product named {product_name}.
    ```
    {product_description}
    ```
    """

def requirements_prompt(product_name, requirement_type):
    """
    Generate a requirements prompt based on the requirement type and product name.
    Args:
        product_name: the name of a product described in a system prompt
        requirement_type: ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"]

    Returns:
        A prompt to use to generate a requirements document
        for the requirement type and product name.
    """
    if requirement_type not in ["Business Problem Statement", "Vision Statement", "Ecosystem map", "RACI Matrix"]:
        raise ValueError(f"Invalid requirement type.")
    if requirement_type == "Business Problem Statement":
        return business_problem_prompt(product_name)
    if requirement_type == "Vision Statement":
        return vision_statement_prompt(product_name)
    if requirement_type == "Ecosystem map":
        return ecosystem_map_prompt(product_name)
    if requirement_type == "RACI Matrix":
        return responsibility_matrix_prompt(product_name)


def business_problem_prompt(product_name):
    """
    Generates a structured prompt for creating a Business Problem Statement.
    """
    return f"""
    **Situation**

    In today's complex financial landscape, individuals face various challenges in managing their finances effectively. Many struggle with making informed decisions about budgeting, saving, investing, and financial planning. While there are numerous resources available, they are often fragmented, difficult to understand, or not tailored to individual needs.

    **Problem**

    The majority of individuals lack financial literacy and personalized guidance, leading to suboptimal financial decisions. There is no comprehensive, AI-driven platform that provides tailored financial advice and document generation in an accessible and user-friendly manner.

    **Implication**

    Without a reliable financial assistant, people may continue making uninformed financial choices, potentially resulting in financial instability, increased debt, and missed opportunities for wealth growth. This gap in financial literacy can also contribute to broader economic challenges.

    **Benefit**

    By addressing this issue, {product_name} empowers users with personalized financial insights, education, and document automation. The platform enhances financial literacy, helps users make better financial decisions, and provides a seamless experience for managing their financial affairs.

    **Vision**

    Imagine a world where everyone has access to an intelligent financial assistant that simplifies complex financial concepts, offers real-time personalized advice, and automates financial document creation. {product_name} aims to bridge the financial literacy gap, ensuring that individuals can confidently navigate their financial future with the right tools and knowledge.
    """


def vision_statement_prompt(product_name):
    """
    Generates a prompt for creating a Vision Statement.
    """
    return f"""
    **For**

    Individuals seeking to navigate their financial futures confidently,

    **Who**

    Desire personalized, trustworthy, and user-friendly financial advice and document generation,

    **The**

    {product_name}

    **Is**

    A cutting-edge AI-powered personal finance assistant

    **That**

    Educates on complex financial topics, offers real-time financial guidance, and generates tailored financial documents to empower users in their financial decisions.

    **Unlike**

    Generic finance websites, overwhelming financial data platforms, and traditional financial consultation.
    """


def ecosystem_map_prompt(product_name):
    """
    Generates a prompt for creating an Ecosystem Map.
    """
    return f"""
    **Ecosystem Map for {product_name}**

    **Central System**: {product_name} Desktop App

    **Direct Interactors**:
    Entities or systems that have a direct interaction with {product_name}.

    1. **End Users**:
       - **Role**: Seek financial advice, generate documents, and learn financial topics.
       - **Interaction**: Input queries, read generated advice, request and receive documents.

    2. **OpenAI API**:
       - **Role**: Generate AI-driven responses for user queries and provide data for financial document generation.
       - **Interaction**: Receive requests from {product_name} and send back AI-generated content.

    3. **Data Storage**:
       - **Role**: Store and retrieve user data, templates, and generated documents.
       - **Interaction**: Accepts and provides data to/from {product_name} on demand.

    **Indirect Interactors**:
    Entities that influence or are influenced by {product_name} but may not directly interact with the app.

    4. **Financial Regulators**:
       - **Role**: Set rules and guidelines on financial advice and data handling.
       - **Interaction**: Influence the structure, content, and policies of the {product_name} app.

    5. **Tech Support**:
       - **Role**: Assist users with technical issues related to the {product_name} application.
       - **Interaction**: Receive user complaints, queries, and feedback regarding the app.

    6. **Financial Content Providers**:
       - **Role**: Source of original financial knowledge that the OpenAI model may have been trained on.
       - **Interaction**: Indirect influence on the quality and accuracy of the advice given through the OpenAI API.

    **Environmental Factors**:

    7. **Economic Climate**:
       - **Role**: The broader economic environment can influence the type and frequency of queries users have.
       - **Interaction**: Indirect influence on user behavior and app utilization.

    8. **Technological Advancements**:
       - **Role**: Influence the development, features, and capabilities of {product_name}.
       - **Interaction**: Changes in technology can lead to updates or alterations in the app's functionalities.
    """


def responsibility_matrix_prompt(product_name):
    """
    Generates a prompt for creating a Responsibility Matrix.
    """
    return f"""
    **Responsibility Matrix for {product_name}**

    | **Tasks/Phases**                  | **Product Owner** | **Development Team** | **QA Team** | **UX/UI Designers** | **End Users** | **Regulatory Compliance Officer** | **Marketing Team** | **Support Team** | **Data Security Expert** |
    |----------------------------------|-------------------|----------------------|-------------|---------------------|---------------|---------------------------------|--------------------|------------------|--------------------------|
    | **Feature Prioritization**       | A                 | R                    | -           | C                   | C             | -                               | -                  | -                | -                        |
    | **App Development**              | C                 | A, R                 | C           | R                   | -             | C                               | -                  | -                | C                        |
    | **Quality Testing**              | C                 | C                    | A, R       | C                   | -             | -                               | -                  | -                | C                        |
    | **UI/UX Design**                 | C                 | C                    | -           | A, R                | C             | -                               | -                  | -                | -                        |
    | **Regulatory Compliance**        | C                 | C                    | -           | -                   | -             | A, R                            | -                  | -                | C                        |
    | **Marketing & Outreach**         | C                 | -                    | -           | -                   | -             | -                               | A, R               | C                | -                        |
    | **Feedback Gathering**           | A                 | C                    | -           | C                   | R             | -                               | C                  | R                | -                        |
    | **Data Protection Measures**     | C                 | C                    | -           | -                   | -             | C                               | -                  | -                | A, R                     |

    Legend:
    - **A** = Accountable (the person who approves the completion of the task)
    - **R** = Responsible (the person or persons who actually complete the task)
    - **C** = Consulted (people who are consulted during the task's completion)
    - **I** = Informed (people who are informed once the task is complete)
    """




