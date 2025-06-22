#
# An iterative refinement loop using a "judge" agent.
#
from typing import Literal
from pydantic import BaseModel, Field
from agents import Agent, Runner, trace, TResponseInputItem
from tinib00k.utils import DEFAULT_LLM, load_and_check_keys
load_and_check_keys()

class CodeEvaluation(BaseModel):
    score: Literal["pass", "fail"] = Field(description="Does the code meet the requirements and seem correct?")
    feedback: str = Field(description="If the score is 'fail', provide concise, actionable feedback for how to fix the code.")

def main():

    # 1. The Generator Agent
    coder_agent = Agent(
        name="Python Coder",
        instructions="You are a skilled Python developer. Write a single Python function to solve the user's request. Do not write any explanations, just the code block.",
        model=DEFAULT_LLM
    )

    # 2. The Judge Agent with a structured output
    reviewer_agent = Agent(
        name="Code Reviewer",
        instructions="You are a senior code reviewer. Evaluate the provided Python function based on the original request. Check for correctness and style. Provide a 'pass' or 'fail' score and feedback.",
        output_type=CodeEvaluation,
        model=DEFAULT_LLM
    )

    # --- Orchestration Loop ---
    task = "a function that takes a list of strings and returns a new list with all strings converted to uppercase."
    # We use a list to build the conversation history for the coder agent
    conversation_history: list[TResponseInputItem] = [{"role": "user", "content": task}]
    max_revisions = 3

    with trace("LLM as a Judge: Code Review"):
        for i in range(max_revisions):
            print(f"\n--- Attempt {i + 1} ---")

            # Step A: Generate the code
            print("Coder Agent is generating code...")
            coder_result = Runner.run_sync(coder_agent, conversation_history)
            generated_code = coder_result.final_output
            print(f"Generated Code:\n```python\n{generated_code}\n```")

            # Add the generated code to its own history
            conversation_history = coder_result.to_input_list()

            # Step B: Judge the code
            print("\nReviewer Agent is evaluating...")
            review_input = f"Original Request: {task}\n\nCode to Review:\n```python\n{generated_code}\n```"
            reviewer_result = Runner.run_sync(reviewer_agent, review_input)

            evaluation: CodeEvaluation = reviewer_result.final_output
            print(f"Reviewer Score: {evaluation.score.upper()}")

            # Step C: Decide whether to loop or break
            if evaluation.score == "pass":
                print("Code passed review! Final code is ready.")
                break
            else:
                print(f"Reviewer Feedback: {evaluation.feedback}")
                # Add the feedback to the coder's conversation history for the next attempt
                feedback_for_coder = f"A reviewer has provided feedback on your last attempt. Please fix it. Feedback: {evaluation.feedback}"
                conversation_history.append({"role": "user", "content": feedback_for_coder})
        else:
            print("\nMax revisions reached. The code did not pass the review.")

if __name__ == "__main__":
    main()