#!/usr/bin/env python3
"""
CLI runner for Open Deep Research that replaces `langgraph dev`.
Reads query from command line args, loads .env, runs deep_researcher,
prints final report, and saves to research_report.md.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Add the src directory to the path so we can import open_deep_research
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from open_deep_research.deep_researcher import deep_researcher


async def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <query>")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    load_dotenv()  # Load environment variables from .env file

    # Invoke the deep researcher with the query as a HumanMessage
    result = await deep_researcher.ainvoke(
        {"messages": [HumanMessage(content=query)]}
    )

    # Extract the final report from the result
    final_report = result.get("final_report", "No report generated.")

    # Print the final report to stdout
    print("\n" + "="*80)
    print("FINAL RESEARCH REPORT")
    print("="*80 + "\n")
    print(final_report)

    # Save the report to research_report.md
    with open("research_report.md", "w", encoding="utf-8") as f:
        f.write(final_report)

    print("\n" + "="*80)
    print(f"Report saved to research_report.md")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())