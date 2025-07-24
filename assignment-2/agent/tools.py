from langchain.agents import tool
import re

# This is a placeholder for a real agent executor that will be passed in.
# This avoids circular dependencies.
_agent_executor = None

def set_agent_executor(agent_executor):
    """Sets the agent executor for the tool to use."""
    global _agent_executor
    _agent_executor = agent_executor

@tool
def find_best_grocery_deal(query: str) -> str:
    """
    Use this tool ONLY for multi-item grocery list queries with a budget,
    like 'Find best deals for a ₹1000 grocery list with 1kg onions, 500g tomatoes, and 1L milk'.
    It finds the cheapest option for each item and calculates the total.
    For single-item queries, use the database directly.
    """
    if _agent_executor is None:
        return "Agent executor not configured for this tool."

    print("--- Using Custom Grocery Deal Tool ---")
    
    # 1. Parse items (simplified parsing)
    items_str = re.findall(r'with (.*)', query, re.IGNORECASE)
    if not items_str:
        return "Could not identify the list of items in your query. Please format as '... with item1, item2, ...'."
    
    items = [item.strip() for item in items_str[0].split(', and')]

    total_cost = 0
    deal_summary = []

    # 2. For each item, invoke the main agent to find the cheapest price
    for item_description in items:
        sub_query = f"What is the lowest price for {item_description} and which single platform has it?"
        response = _agent_executor.invoke({"input": sub_query})
        output = response.get('output', '')
        
        # 3. Parse the sub-response and aggregate results
        try:
            price_match = re.search(r"[₹$](\d+\.?\d*)", output)
            platform_match = re.search(r"on (\w+)", output, re.IGNORECASE)
            
            if price_match and platform_match:
                price = float(price_match.group(1))
                platform = platform_match.group(1)
                total_cost += price
                deal_summary.append(f"- {item_description} on **{platform}** for **₹{price:.2f}**")
            else:
                 deal_summary.append(f"- Could not find a specific deal for {item_description}. Got: {output}")
        except Exception as e:
            deal_summary.append(f"- Error finding deal for {item_description}: {e}")

    # 4. Format the final output
    budget_match = re.search(r"[₹$](\d+)", query)
    budget = float(budget_match.group(1)) if budget_match else 0
    
    result = "### Grocery Deal Summary:\n" + "\n".join(deal_summary)
    result += f"\n\n**Total Estimated Cost: ₹{total_cost:.2f}**"
    
    if budget > 0:
        if total_cost <= budget:
            result += f"\n✅ This is within your budget of ₹{budget:.2f}."
        else:
            result += f"\n❌ This is OVER your budget of ₹{budget:.2f} by ₹{total_cost - budget:.2f}."
            
    return result