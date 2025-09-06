import asyncio
from typing import List, Dict, Any, Optional
from src.core.knowledge_logger import log_to_knowledge_vault
from datetime import datetime
import re

# This would ideally be a persistent storage of logs
_simulated_log_store: List[Dict[str, Any]] = []
_latest_lumen_insights: Optional[Dict[str, Any]] = None

async def analyze_logs_for_insights(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Simulates Lumen Protocol's analysis of logs to generate insights."""
    global _latest_lumen_insights

    print("[LUMEN_ANALYZER] Analyzing logs for insights...")
    
    total_events = len(logs)
    failed_events = [log for log in logs if log.get('log_level') == 'ERROR']
    warning_events = [log for log in logs if log.get('log_level') == 'WARNING']

    insights = {
        "total_events_processed": total_events,
        "error_rate": len(failed_events) / total_events if total_events > 0 else 0,
        "warning_rate": len(warning_events) / total_events if total_events > 0 else 0,
        "common_errors": {},
        "suggested_improvements": []
    }

    # Simulate identifying common errors
    for event in failed_events:
        event_type = event.get('event_type', 'unknown')
        insights["common_errors"][event_type] = insights["common_errors"].get(event_type, 0) + 1
    
    # Simulate suggesting improvements based on insights
    if insights["error_rate"] > 0.1:
        insights["suggested_improvements"].append("Review agents with high error rates for stability improvements.")
    if insights["warning_rate"] > 0.2:
        insights["suggested_improvements"].append("Investigate sources of warnings to prevent future issues.")
    if "code_generation_failed_early_exit" in insights["common_errors"]:
        insights["suggested_improvements"].append("Enhance code generation model's robustness for complex ideas.")

    await log_to_knowledge_vault("lumen_analysis_completed", insights, log_level="INFO", source_agent="LumenAnalyzer")
    _latest_lumen_insights = insights # Store the latest insights
    return insights

async def update_adaptation_loop(insights: Dict[str, Any]):
    """Updates the 02_ADAPTATION_LOOP.md based on Lumen insights."""
    print("[LUMEN_ANALYZER] Updating Adaptation Loop with insights...")
    
    adaptation_loop_path = "/Users/corenzo/Documents/Code/02_ADAPTATION_LOOP.md"
    
    # Read current content
    current_content_response = default_api.read_file(absolute_path=adaptation_loop_path)
    current_content = current_content_response['read_file_response']['content']

    # Prepare new entries
    shipped_entry = f"- Lumen analysis performed. Error Rate: {insights.get('error_rate'):.2f}, Warning Rate: {insights.get('warning_rate'):.2f}."
    learned_entry = "\n".join([f"- {s}" for s in insights.get('suggested_improvements', ["No specific improvements suggested."]])

    # Find the current week's entry or create a new one
    today = datetime.now().strftime("%B %d, %Y")
    week_of_pattern = r"## Week of (.*?)\n"
    
    match = re.search(week_of_pattern, current_content)
    
    new_content = current_content
    if match:
        # Append to existing week if it's the same week (simplified check)
        # For a real system, this would involve more robust date comparison
        if today in match.group(0):
            # Append to existing shipped and learned sections
            new_content = re.sub(r"\n\*\*Shipped:\*\*.*", lambda m: m.group(0) + f"\n  {shipped_entry}", new_content, count=1)
            new_content = re.sub(r"\n\*\*Learned:\*\*.*", lambda m: m.group(0) + f"\n  {learned_entry}", new_content, count=1)
        else:
            # Add a new week entry at the top
            new_week_entry = f"\n## Week of {today}\n**Shipped:** {shipped_entry}\n**Learned:** {learned_entry}\n**Blockers:** [Current challenges]\n**KPIs:** [Metric updates]\n"
            new_content = re.sub(r"# ADAPTATION LOOP", f"# ADAPTATION LOOP\n\n{new_week_entry}", new_content, count=1)
    else:
        # If no week entry found, add the first one
        new_week_entry = f"\n## Week of {today}\n**Shipped:** {shipped_entry}\n**Learned:** {learned_entry}\n**Blockers:** [Current challenges]\n**KPIs:** [Metric updates]\n"
        new_content = re.sub(r"# ADAPTATION LOOP", f"# ADAPTATION LOOP\n\n{new_week_entry}", new_content, count=1)

    # Write updated content back to the file
    default_api.write_file(file_path=adaptation_loop_path, content=new_content)
    await log_to_knowledge_vault("adaptation_loop_updated", {"week_of": today, "shipped_entry": shipped_entry, "learned_entry": learned_entry}, log_level="INFO", source_agent="LumenAnalyzer")

async def run_lumen_feedback_loop():
    """Simulates the continuous Lumen feedback loop."""
    while True:
        await asyncio.sleep(10) # Simulate periodic analysis (e.g., every 10 seconds for stress test)
        print("\n[LUMEN_ANALYZER] Initiating periodic Lumen feedback loop...")
        
        current_logs = list(_simulated_log_store) # Get a snapshot of logs
        _simulated_log_store.clear() # Clear for next cycle (simplified)

        if current_logs:
            insights = await analyze_logs_for_insights(current_logs)
            await update_adaptation_loop(insights)
        else:
            print("[LUMEN_ANALYZER] No new logs to analyze.")

# Function to allow external components to add logs to the simulated store
def add_log_to_simulated_store(log_entry: Dict[str, Any]):
    _simulated_log_store.append(log_entry)

def get_latest_lumen_insights() -> Optional[Dict[str, Any]]:
    """Returns the latest insights generated by the Lumen Analyzer."""
    return _latest_lumen_insights
