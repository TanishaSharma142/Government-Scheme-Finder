import json
from smolagents import CodeAgent, HfApiModel, tool

# --- 1. DEFINE THE TOOL ---
@tool
def find_schemes(age: int, gender: str, income: int, state: str, occupation: str, disability_percent: int) -> str:
    """
    Searches the schemes.json file to find government schemes the user is eligible for.
    
    Args:
        age: User's age in years.
        gender: User's gender ('male', 'female', 'other').
        income: Annual family income in Rupees.
        state: User's home state (e.g., 'Uttar Pradesh', 'Telangana').
        occupation: User's job (e.g., 'student', 'farmer', 'street_vendor', 'unemployed').
        disability_percent: Percentage of disability (0 if none).
    """
    try:
        with open('schemes.json', 'r', encoding='utf-8') as f:
            schemes = json.load(f)
    except FileNotFoundError:
        return "Error: schemes.json file not found."

    eligible = []
    
    for scheme in schemes:
        cond = scheme.get('conditions', {})
        
        # Check Age
        if 'min_age' in cond and age < cond['min_age']: continue
        if 'max_age' in cond and age > cond['max_age']: continue
        
        # Check Income (skip if scheme has no income limit)
        if 'max_income' in cond and income > cond['max_income']: continue
        
        # Check Gender
        if 'gender' in cond and cond['gender'].lower() != gender.lower(): continue
        
        # Check State
        if 'state' in cond and cond['state'].lower() != state.lower(): continue
        
        # Check Disability
        if 'min_disability' in cond and disability_percent < cond['min_disability']: continue

        # Check Occupation (Handle lists or single strings)
        if 'occupation' in cond:
            req_occ = cond['occupation']
            if isinstance(req_occ, list):
                if occupation.lower() not in [o.lower() for o in req_occ]: continue
            elif req_occ.lower() != occupation.lower(): continue

        # If we passed all checks, add to list
        eligible.append(f"- {scheme['name']} (Benefit: {scheme['benefits']})")

    if not eligible:
        return "No schemes found for this profile."
    
    return "\n".join(eligible)

# --- 2. SETUP THE AGENT ---
# HfApiModel uses free inference API (default model is usually Qwen or Zephyr)
model = HfApiModel()

agent = CodeAgent(
    tools=[find_schemes], 
    model=model
)

# --- 3. RUN THE AGENT ---
# You can change this query to test different users
user_query = "I am a 20 year old female student from Uttar Pradesh. My family income is 1.5 Lakh. I am OBC."

print(f"User Query: {user_query}")
print("Agent is thinking...\n")

result = agent.run(user_query)

print("\n--- FINAL ANSWER ---")
print(result)
