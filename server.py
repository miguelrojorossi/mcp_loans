import asyncio
import os
import random
import re
from fastmcp import FastMCP

mcp = FastMCP("LoanMCPTools")

@mcp.tool()
def calculate_monthly_installment(amount: float, months: int, annual_rate_percentage: float) -> str:
    """Calculates the monthly payment for a Santander Personal Loan."""
    if months <= 0 or amount <= 0:
        return "Error: Duration and amount must be positive."

    # Prevent division by zero if interest is 0%
    if annual_rate_percentage == 0:
        payment = amount / months
    else:
        monthly_rate = (annual_rate_percentage / 100) / 12
        payment = (amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    
    total_interest = (payment * months) - amount
    return (f"CALCULATION_SUCCESS:\n- Monthly Payment: €{payment:,.2f}\n"
            f"- Total Interest: €{total_interest:,.2f}")

@mcp.tool()
def get_customer_interest_rate(dni: str) -> str:
    """Retrieves the personalized interest rate for a customer based on their DNI."""
    if not re.match(r"^\d{8}[A-Za-z]$", dni):
        return "ERROR: Invalid DNI format."

    segment_rates = {"Select": 1.5, "Standard": 5.5, "Student": 3.0}
    assigned_segment = random.choice(list(segment_rates.keys()))
    return f"SUCCESS: {dni.upper()} is '{assigned_segment}' at {segment_rates[assigned_segment]}%."

if __name__ == "__main__":
    # Cloud Run provides the PORT environment variable
    port = int(os.getenv("PORT", 8080))
    
    # Using SSE (Server-Sent Events) via streamable-http is standard for Cloud Run MCP
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=port
        )
    )