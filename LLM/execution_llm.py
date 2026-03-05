import json
import re
from llm_setup import llm


def generate_execution_explanations(raw, detection, context, authority, execution_result):
    """
    Generate AI explanations for execution layer results using LLM
    """

    # Determine execution type based on result structure
    if "containment_triggered" in execution_result:
        execution_type = "CONTAINMENT"
        metrics = {
            "containment_triggered": execution_result.get("containment_triggered"),
            "actions_executed": execution_result.get("actions_executed", []),
            "status": execution_result.get("status")
        }
    elif "escalation" in execution_result:
        execution_type = "HUMAN_REVIEW"
        metrics = {
            "escalation": execution_result.get("escalation"),
            "assigned_queue": execution_result.get("assigned_queue"),
            "ticket_priority": execution_result.get("ticket_priority"),
            "device": execution_result.get("device"),
            "status": execution_result.get("status")
        }
    elif "monitoring_enabled" in execution_result:
        execution_type = "ADAPTIVE_MONITORING"
        metrics = {
            "monitoring_enabled": execution_result.get("monitoring_enabled"),
            "monitoring_duration_hours": execution_result.get("monitoring_duration_hours"),
            "log_level": execution_result.get("log_level"),
            "status": execution_result.get("status")
        }
    elif "action" in execution_result and execution_result.get("action") == "NO_ACTION_REQUIRED":
        execution_type = "SAFE_PASS"
        metrics = {
            "action": execution_result.get("action"),
            "log_entry": execution_result.get("log_entry"),
            "status": execution_result.get("status")
        }
    else:
        execution_type = "UNKNOWN"
        metrics = execution_result

    prompt = f"""
You are a cybersecurity SOC analyst specializing in incident response execution and automated remediation.

Explain the following execution layer results clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.
- Explain the specific execution actions taken based on the context.

Return ONLY JSON in this format:
"""

    if execution_type == "CONTAINMENT":
        prompt += f"""
{{
"containment_triggered": "Explanation...",
"actions_executed": "Explanation...",
"status": "Explanation..."
}}

Execution Type: AUTOMATED CONTAINMENT

Containment Triggered = {metrics.get("containment_triggered")}
Actions Executed = {metrics.get("actions_executed")}
Status = {metrics.get("status")}
"""
    elif execution_type == "HUMAN_REVIEW":
        prompt += f"""
{{
"escalation": "Explanation...",
"assigned_queue": "Explanation...",
"ticket_priority": "Explanation...",
"status": "Explanation..."
}}

Execution Type: HUMAN ANALYST ESCALATION

Escalation = {metrics.get("escalation")}
Assigned Queue = {metrics.get("assigned_queue")}
Ticket Priority = {metrics.get("ticket_priority")}
Device = {metrics.get("device")}
Status = {metrics.get("status")}
"""
    elif execution_type == "ADAPTIVE_MONITORING":
        prompt += f"""
{{
"monitoring_enabled": "Explanation...",
"monitoring_duration_hours": "Explanation...",
"log_level": "Explanation...",
"status": "Explanation..."
}}

Execution Type: ADAPTIVE MONITORING

Monitoring Enabled = {metrics.get("monitoring_enabled")}
Monitoring Duration Hours = {metrics.get("monitoring_duration_hours")}
Log Level = {metrics.get("log_level")}
Status = {metrics.get("status")}
"""
    elif execution_type == "SAFE_PASS":
        prompt += f"""
{{
"action": "Explanation...",
"log_entry": "Explanation...",
"status": "Explanation..."
}}

Execution Type: SAFE PASS

Action = {metrics.get("action")}
Log Entry = {metrics.get("log_entry")}
Status = {metrics.get("status")}
"""

    prompt += f"""

Authority Context:
Final Decision: {authority.get("final_decision")}
Execution Mode: {authority.get("execution_mode")}
Severity Level: {authority.get("severity_level")}
Decision Confidence: {authority.get("decision_confidence")}

Device Context:
Device ID: {raw.get("device_id")}
Department: {raw.get("department")}
Criticality Level: {raw.get("criticality_level")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("EXECUTION LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == execution_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("EXECUTION LLM ERROR:", e)

        # Fallback explanations based on execution type
        if execution_type == "CONTAINMENT":
            return {
                "containment_triggered": (
                    "Automated containment was triggered in response to critical security incidents requiring "
                    "immediate isolation to prevent threat propagation. This action ensures the affected system "
                    "is immediately quarantined from the network to contain potential damage."
                ),

                "actions_executed": (
                    "Specific containment actions were executed including network isolation, privilege revocation, "
                    "traffic blocking, and forensic preservation. These coordinated measures work together to "
                    "immediately neutralize the threat while preserving evidence for post-incident analysis."
                ),

                "status": (
                    "Containment status indicates the current state of the isolation and neutralization process. "
                    "Successful containment ensures the threat is contained and the system is secured pending "
                    "further investigation and remediation."
                )
            }
        elif execution_type == "HUMAN_REVIEW":
            return {
                "escalation": (
                    "Incident escalation to human analysts was triggered due to complexity or uncertainty requiring "
                    "expert human judgment. This ensures critical decisions are made by experienced security "
                    "professionals when automated systems cannot provide sufficient confidence."
                ),

                "assigned_queue": (
                    "The incident was assigned to the appropriate analyst queue based on severity and specialization. "
                    "Tier-2 analysts handle complex cases requiring deeper investigation and expert analysis beyond "
                    "automated detection capabilities."
                ),

                "ticket_priority": (
                    "High priority was assigned to ensure rapid response and investigation by security analysts. "
                    "This prioritization ensures critical incidents receive immediate attention and appropriate "
                    "resources for timely resolution."
                ),

                "status": (
                    "The incident is currently awaiting human review and analysis. This status indicates the "
                    "case has been properly escalated and is queued for expert examination and decision making."
                )
            }
        elif execution_type == "ADAPTIVE_MONITORING":
            return {
                "monitoring_enabled": (
                    "Adaptive monitoring was enabled to provide enhanced surveillance of suspicious but not "
                    "immediately critical activities. This approach allows for real-time observation while "
                    "gathering additional context before deciding on containment actions."
                ),

                "monitoring_duration_hours": (
                    "Extended monitoring duration was established to allow sufficient time for threat pattern "
                    "analysis and behavior observation. This period enables security teams to make informed "
                    "decisions based on comprehensive activity monitoring."
                ),

                "log_level": (
                    "Elevated logging level was activated to capture detailed security events and system activities. "
                    "This enhanced logging provides comprehensive audit trails for post-incident analysis and "
                    "threat hunting activities."
                ),

                "status": (
                    "The system is currently under active observation with enhanced monitoring capabilities. "
                    "This status indicates the incident is being closely tracked while additional intelligence "
                    "is gathered for final disposition."
                )
            }
        else:  # SAFE_PASS
            return {
                "action": (
                    "No action was required as the event was determined to be safe after comprehensive SOC "
                    "evaluation. This determination was made based on thorough risk assessment and confidence "
                    "in the benign nature of the detected activity."
                ),

                "log_entry": (
                    "The safe determination was logged for audit and compliance purposes. This logging ensures "
                    "complete traceability of security decisions and maintains records for future analysis "
                    "and pattern recognition."
                ),

                "status": (
                    "The event was cleared after full security evaluation and poses no threat. This status "
                    "indicates the incident has been resolved and no further action is required."
                )
            }
