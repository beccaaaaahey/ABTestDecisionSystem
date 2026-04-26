# %%
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY").strip()

genai.configure(api_key=api_key)

try:
    print("--- Finding available models ---")
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if not available_models:
        print("Error: Your API Key currently has no access to any models. Please check your Google AI Studio account status.")
    else:
        target_model = available_models[0]
        print(f"Successfully detected available model: {target_model}")
        
        model = genai.GenerativeModel(target_model)
        response = model.generate_content("System confirmed")
        
        print(f"\nSuccessfully completed!\nAI Response: {response.text}")

except Exception as e:
    print(f"Attempt failed. Error details:\n{e}")
    
# Read the statistical summary results from the text file
with open("stats_summary.txt", "r") as f:
    summary_content = f.read()

# Read the pytorch results from the text file
with open("ml_insights.txt", "r") as f:
    ml_insights = f.read()

tuning_log = f"""
ml results:
{ml_insights}
### ML Model Architecture & Performance:
1. **Conversion Model (convertPredictor)**:
   - Architecture: MLP (3 -> 16 -> 8 -> 1)
   - Optimizer: Adam (LR: 0.01, Epochs: 100)

2. **Retention Model (retentionPredictor)**:
   - Architecture: MLP (3 -> 64 -> 32 -> 1)
   - Optimizer: Adam (LR: 0.001, Epochs: 300)
   - Optimization: Implemented 'ReduceLROnPlateau' scheduler.
   
###Model Tuning Insights:
- Experimented with increasing hidden layers (32-16-8) which improved baseline accuracy.
- Implemented ReduceLROnPlateau; loss stabilized but accuracy plateaued.
- Conclusion: Current features (hesitation, past_sessions) have reached their predictive limit.
"""

prompt1 = f'''You are a Senior Product Data Scientist working on an A/B testing experiment.
We have two groups: control (Soft Paywall) and treatment (Hard Paywall). 
Here are the key results from our statistical analysis:
{summary_content}
Please provide a clear recommendation on whether to implement the hard paywall based on these results.
The result will involve several points:
(1) Explain the experiment results in simple terms
(2) Is the experiment reliable?
(3) What are the potential risks of implementing the hard paywall? What should we do if retention rate decline but conversion rate increase?
(4) Would you recommend launching the hard paywall?
(5) What are the next steps for business stratigies and further analysis or testing?'''

prompt2 = f'''You are a Senior Product Data Scientist working on an A/B testing experiment.
{tuning_log}
(1) What does the model tuning process tell us about the data and features we have?
(2) How should we interpret the model tuning results in the context of our A/B testing experiment?
(3) Any recommendations for future model improvements or feature engineering based on the tuning insights?
'''

response = model.generate_content(prompt1)
print("\n--- Completed!---")
print(f"\nAI Response:\n{response.text}")

response2 = model.generate_content(prompt2)
print("\n--- Completed!---")
print(f"\nAI Response:\n{response2.text}")

with open("AI_Decision_Report.md", "w", encoding="utf-8") as f:
    f.write(f"# from {target_model}\n\n")
    f.write(f"# 2026-04-20\n\n")
    f.write("--- \n\n")
    f.write(f"# Prompt1\n\n")
    f.write(prompt1 + "\n\n")
    f.write(response.text)
    f.write("--- \n\n")
    
    f.write(f"# Prompt2\n\n")
    f.write(prompt2 + "\n\n")
    f.write(response2.text)

print("\n Response saved to final_decision_report.md")
# %%
