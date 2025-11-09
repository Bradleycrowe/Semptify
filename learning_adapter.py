"""
Learning Adapter - Generates dashboard components based on user data and learning engine
Analyzes user stage, location, issue type, and history to populate dashboard
"""

from dashboard_components import (
    DashboardBuilder, RightsComponent, InformationComponent,
    InputComponent, NextStepsComponent, TimelineComponent
)
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class LearningAdapter:
    """Adapts learning engine output to dashboard components"""

    # User stages (from learning engine)
    STAGE_SEARCHING = "SEARCHING"
    STAGE_HAVING_TROUBLE = "HAVING_TROUBLE"
    STAGE_MOVING_IN = "MOVING_IN"
    STAGE_CONFLICT = "CONFLICT"
    STAGE_LEGAL = "LEGAL"

    # Issue types (from learning engine)
    ISSUE_TYPES = {
        "rent": "Rent & Payment",
        "maintenance": "Maintenance & Repairs",
        "eviction": "Eviction",
        "discrimination": "Discrimination",
        "harassment": "Harassment",
        "deposit": "Security Deposit",
        "move": "Moving & Lease"
    }

    # Location-specific rights (simplified - would be expanded with real legal data)
    JURISDICTION_RIGHTS = {
        "MN": {
            "rent": [
                {
                    "title": "Rent Control",
                    "description": "Minnesota limits how much rent can increase in some areas. Check local ordinances.",
                    "source": "MN Statutes §§ 507.18"
                },
                {
                    "title": "Notice to Vacate",
                    "description": "Landlord must provide 30 days written notice for non-renewal or termination.",
                    "source": "MN Statutes § 504B.135"
                }
            ],
            "maintenance": [
                {
                    "title": "Habitability Standards",
                    "description": "Landlord must maintain the property in safe, sanitary condition suitable for occupation.",
                    "source": "MN Statutes § 504B.161"
                },
                {
                    "title": "Repair Rights",
                    "description": "You have the right to request repairs. Landlord has 14 days to make emergency repairs.",
                    "source": "MN Statutes § 504B.211"
                }
            ],
            "eviction": [
                {
                    "title": "Eviction Notice",
                    "description": "Landlord must provide written notice with specific legal reason before eviction.",
                    "source": "MN Statutes § 504B.135"
                }
            ]
        },
        "CA": {
            "rent": [
                {
                    "title": "Just Cause for Eviction",
                    "description": "Landlord must have legal cause to evict. Economic hardship is not cause.",
                    "source": "CA Civil Code § 1946.2"
                }
            ]
        }
    }

    def __init__(self, user_data: Dict[str, Any]):
        """
        Initialize adapter with user data

        user_data should contain:
        - user_id: string
        - location: string (state/city)
        - issue_type: string (rent, maintenance, eviction, etc.)
        - stage: string (SEARCHING, HAVING_TROUBLE, CONFLICT, etc.)
        - history: list of past interactions
        """
        self.user_data = user_data
        self.user_id = user_data.get("user_id", "unknown")
        self.location = user_data.get("location", "MN")  # Default to MN
        self.issue_type = user_data.get("issue_type", "rent")
        self.stage = user_data.get("stage", self.STAGE_SEARCHING)
        self.history = user_data.get("history", [])

    def build_dashboard(self) -> DashboardBuilder:
        """Generate complete dashboard with all 5 rows populated"""
        builder = DashboardBuilder()

        # Row 1: Rights (always populated)
        rights_component = self._build_rights_component()
        builder.add_component(rights_component, 1)

        # Row 2: Information (always populated)
        info_component = self._build_information_component()
        builder.add_component(info_component, 2)

        # Row 3: Input (scales based on stage)
        input_component = self._build_input_component()
        builder.add_component(input_component, 3)

        # Row 4: Next Steps (always populated)
        steps_component = self._build_next_steps_component()
        builder.add_component(steps_component, 4)

        # Row 5: Timeline (always populated)
        timeline_component = self._build_timeline_component()
        builder.add_component(timeline_component, 5)

        return builder

    def _build_rights_component(self) -> RightsComponent:
        """Build Row 1: Legal rights specific to location and issue"""
        component = RightsComponent()
        component.jurisdiction = self.location
        component.issue_type = self.ISSUE_TYPES.get(self.issue_type, self.issue_type)

        # Get jurisdiction-specific rights
        # Extract state from location (e.g., "Minneapolis, MN" -> "MN")
        parts = self.location.split(",")
        if len(parts) >= 2:
            jurisdiction_key = parts[1].strip().upper()[:2]  # Get state from right side
        else:
            jurisdiction_key = parts[0].strip().upper()[:2]  # Fallback to city

        # Get the state dict, default to MN
        state_rights = self.JURISDICTION_RIGHTS.get(jurisdiction_key, self.JURISDICTION_RIGHTS.get("MN", {}))

        # Get rights for this issue type
        rights_list = state_rights.get(self.issue_type, [])

        for right in rights_list:
            component.add_right(
                title=right["title"],
                description=right["description"],
                source=right.get("source", "")
            )

        # Add generic tenant rights
        if not rights_list:
            component.add_right(
                title="Tenant Rights",
                description="You have basic protections under tenant law. Learn what they are.",
                source="State Tenant Rights"
            )

        return component

    def _build_information_component(self) -> InformationComponent:
        """Build Row 2: Smart guidance and warnings"""
        component = InformationComponent()

        # Stage-specific guidance
        if self.stage == self.STAGE_SEARCHING:
            component.add_guidance(
                title="Take Your Time",
                description="Review lease terms carefully before signing. Don't feel rushed."
            )
            component.add_guidance(
                title="Document Everything",
                description="Take photos of the property condition before moving in."
            )

        elif self.stage == self.STAGE_HAVING_TROUBLE:
            component.add_warning(
                title="Act Quickly",
                description="Tenant disputes often have time limits. Document issues now.",
                severity="warning"
            )
            component.add_guidance(
                title="Send Written Notice",
                description="Always use written communication (email, certified mail) with landlord."
            )

        elif self.stage == self.STAGE_CONFLICT:
            component.add_warning(
                title="Legal Implications",
                description="Disputes may affect your rental history. Consider legal help.",
                severity="critical"
            )
            component.add_guidance(
                title="Know Your Options",
                description="Understand mediation, small claims, and formal legal processes."
            )

        elif self.stage == self.STAGE_LEGAL:
            component.add_warning(
                title="Legal Process",
                description="You may be involved in court proceedings. Keep all documentation.",
                severity="critical"
            )
            component.add_guidance(
                title="Get Professional Help",
                description="Consider consulting a lawyer or legal aid organization."
            )

        # Issue-specific warnings
        if self.issue_type == "eviction":
            component.add_warning(
                title="Eviction Risk",
                description="Eviction actions move quickly. Respond to all notices immediately.",
                severity="critical"
            )

        elif self.issue_type == "maintenance":
            component.add_warning(
                title="Health & Safety",
                description="Maintenance issues can affect habitability. Document everything.",
                severity="warning"
            )

        return component

    def _build_input_component(self) -> InputComponent:
        """Build Row 3: Flexible input boxes that scale based on stage"""
        component = InputComponent()

        # Generic fields (always present)
        component.add_field(
            "current_status",
            "Current Status",
            field_type="select",
            options=["Searching", "Just moved in", "Having issues", "In conflict", "Legal action"],
            required=True
        )

        # Stage-specific input fields
        if self.stage == self.STAGE_SEARCHING:
            component.add_field(
                "lease_terms",
                "What concerns do you have about the lease?",
                field_type="textarea",
                placeholder="E.g., rent increase clause, maintenance responsibilities..."
            )
            component.add_field(
                "move_date",
                "Planned move-in date",
                field_type="date"
            )

        elif self.stage == self.STAGE_HAVING_TROUBLE:
            component.add_field(
                "issue_description",
                "Describe the issue",
                field_type="textarea",
                placeholder="Be specific with dates and details...",
                required=True
            )
            component.add_field(
                "issue_duration",
                "How long has this been an issue?",
                field_type="select",
                options=["Less than 1 week", "1-2 weeks", "1 month", "2+ months"],
                required=True
            )
            component.add_field(
                "landlord_contacted",
                "Have you contacted the landlord?",
                field_type="select",
                options=["Not yet", "Verbally", "In writing", "No response"],
                required=True
            )

        elif self.stage == self.STAGE_CONFLICT:
            component.add_field(
                "attempted_resolution",
                "Have you attempted any resolution?",
                field_type="select",
                options=["Direct negotiation", "Mediation", "Not yet"],
                required=True
            )
            component.add_field(
                "documentation",
                "What documentation do you have?",
                field_type="textarea",
                placeholder="Emails, photos, repair requests, etc."
            )

        elif self.stage == self.STAGE_LEGAL:
            component.add_field(
                "legal_action_type",
                "Type of legal action",
                field_type="select",
                options=["Small claims", "Eviction defense", "Complaint filed", "Other"],
                required=True
            )
            component.add_field(
                "court_date",
                "Court date (if applicable)",
                field_type="date"
            )

        # Issue-specific fields
        if self.issue_type == "rent":
            component.add_field(
                "monthly_rent",
                "Monthly rent amount",
                field_type="text",
                placeholder="E.g., $1200"
            )

        elif self.issue_type == "eviction":
            component.add_field(
                "notice_received",
                "When did you receive the notice?",
                field_type="date",
                required=True
            )

        return component

    def _build_next_steps_component(self) -> NextStepsComponent:
        """Build Row 4: Action recommendations"""
        component = NextStepsComponent()

        step_num = 1

        # Stage-specific next steps
        if self.stage == self.STAGE_SEARCHING:
            component.add_step(
                step_num, "Review Lease Carefully",
                "Read every page. Look for terms about maintenance, increases, and termination.",
                action_url="/resources/lease-checklist",
                action_text="Lease Checklist"
            )
            step_num += 1

            component.add_step(
                step_num, "Inspect the Property",
                "Take photos/video of the entire property condition before signing.",
                action_url="/resources/inspection-guide",
                action_text="Inspection Guide"
            )
            step_num += 1

            component.add_step(
                step_num, "Document Everything",
                "Keep a copy of the signed lease and all communications.",
                action_url="/vault",
                action_text="Document Storage"
            )

        elif self.stage == self.STAGE_HAVING_TROUBLE:
            component.add_step(
                step_num, "Document the Issue",
                "Take photos/videos and note dates and times of the problem.",
                action_url="/resources/documentation-guide",
                action_text="How to Document"
            )
            step_num += 1

            component.add_step(
                step_num, "Contact Landlord in Writing",
                "Send a certified letter or email requesting repair/resolution.",
                action_url="/resources/letter-templates",
                action_text="Letter Templates"
            )
            step_num += 1

            component.add_step(
                step_num, "Wait for Response",
                "Give landlord legally required time to respond (varies by state).",
                action_url="/resources/timelines",
                action_text="Legal Timelines"
            )

        elif self.stage == self.STAGE_CONFLICT:
            component.add_step(
                step_num, "Try Mediation",
                "Many disputes can be resolved through neutral third party.",
                action_url="/resources/mediation",
                action_text="Find Mediation"
            )
            step_num += 1

            component.add_step(
                step_num, "Gather All Evidence",
                "Collect lease, communications, photos, witness statements.",
                action_url="/vault",
                action_text="Evidence Storage"
            )
            step_num += 1

            component.add_step(
                step_num, "Consult Legal Help",
                "Consider free legal aid or tenant advocacy organizations.",
                action_url="/resources/legal-help",
                action_text="Find Legal Help"
            )

        elif self.stage == self.STAGE_LEGAL:
            component.add_step(
                step_num, "Prepare Your Case",
                "Organize all evidence and prepare statements.",
                action_url="/resources/case-preparation",
                action_text="Case Preparation"
            )
            step_num += 1

            component.add_step(
                step_num, "Attend All Proceedings",
                "Appear on time for all court dates and meetings.",
                action_url="/resources/court-guide",
                action_text="Court Guide"
            )
            step_num += 1

            component.add_step(
                step_num, "Follow Up",
                "Keep records of all court decisions and enforcement.",
                action_url="/vault",
                action_text="Keep Records"
            )

        return component

    def _build_timeline_component(self) -> TimelineComponent:
        """Build Row 5: Important dates and timeline"""
        component = TimelineComponent()

        today = datetime.now().date()

        # Stage-specific timeline events
        if self.stage == self.STAGE_SEARCHING:
            if hasattr(self.user_data, 'get') and self.user_data.get('move_date'):
                component.add_event(
                    self.user_data['move_date'],
                    "Planned Move-in",
                    "Your intended move date",
                    event_type="deadline"
                )

        elif self.stage == self.STAGE_HAVING_TROUBLE:
            # Add a generic response deadline (14 days from today for example)
            deadline = today + timedelta(days=14)
            component.add_event(
                deadline.isoformat(),
                "Follow-up Deadline",
                "If landlord doesn't respond, consider next action",
                event_type="deadline"
            )

        elif self.stage == self.STAGE_CONFLICT:
            # Add mediation deadline
            deadline = today + timedelta(days=30)
            component.add_event(
                deadline.isoformat(),
                "Mediation Opportunity Window",
                "Consider attempting mediation within this timeframe",
                event_type="deadline"
            )

        elif self.stage == self.STAGE_LEGAL:
            if hasattr(self.user_data, 'get') and self.user_data.get('court_date'):
                component.add_event(
                    self.user_data['court_date'],
                    "Court Date",
                    "Important: You must appear on this date",
                    event_type="hearing"
                )

            # Add a preparation deadline (1 week before court)
            if hasattr(self.user_data, 'get') and self.user_data.get('court_date'):
                court_date = datetime.fromisoformat(self.user_data['court_date']).date()
                prep_deadline = court_date - timedelta(days=7)
                component.add_event(
                    prep_deadline.isoformat(),
                    "Case Preparation Deadline",
                    "Complete all case preparation by this date",
                    event_type="deadline"
                )

        # Add issue-specific timeline
        if self.issue_type == "rent":
            # Next rent payment
            next_payment = today.replace(day=1) + timedelta(days=32)
            next_payment = next_payment.replace(day=1)
            component.add_event(
                next_payment.isoformat(),
                "Next Rent Payment Due",
                "Pay on time to maintain good standing",
                event_type="payment",
                related_amount="$" + str(self.user_data.get('monthly_rent', '????'))
            )

        elif self.issue_type == "eviction":
            if hasattr(self.user_data, 'get') and self.user_data.get('notice_date'):
                notice_date = datetime.fromisoformat(self.user_data['notice_date']).date()
                response_deadline = notice_date + timedelta(days=5)
                component.add_event(
                    response_deadline.isoformat(),
                    "Response Deadline",
                    "You must respond to eviction notice by this date",
                    event_type="deadline"
                )

        # Add today as reference point
        component.add_event(
            today.isoformat(),
            "Today",
            "Current date for reference",
            event_type="note"
        )

        return component


def generate_dashboard_for_user(user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to generate dashboard JSON for a user

    Args:
        user_id: User ID
        user_data: Dict with user info (location, issue_type, stage, history, etc.)

    Returns:
        Dict ready to send to frontend
    """
    user_data['user_id'] = user_id
    adapter = LearningAdapter(user_data)
    dashboard = adapter.build_dashboard()

    return {
        "user_id": user_id,
        "stage": adapter.stage,
        "issue_type": adapter.issue_type,
        "location": adapter.location,
        "dashboard": dashboard.to_json()
    }
