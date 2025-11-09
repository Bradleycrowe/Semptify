"""
Dashboard Component System
Renders personalized dashboard components based on learning engine analysis
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class DashboardComponent(ABC):
    """Base class for all dashboard components"""

    def __init__(self, component_id: str, title: str):
        self.component_id = component_id
        self.title = title
        self.content = None
        self.css_class = ""

    @abstractmethod
    def to_html(self) -> str:
        """Convert component to HTML"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to JSON-serializable dict"""
        return {
            "id": self.component_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "content": self.content,
            "html": self.to_html()
        }


class RightsComponent(DashboardComponent):
    """ROW 1: Legal rights specific to location and issue"""

    def __init__(self):
        super().__init__("row_1_rights", "Your Legal Rights")
        self.css_class = "component-full-width rights-box"
        self.rights_list = []
        self.jurisdiction = ""
        self.issue_type = ""

    def add_right(self, title: str, description: str, source: str = ""):
        """Add a legal right to display"""
        self.rights_list.append({
            "title": title,
            "description": description,
            "source": source
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to JSON-serializable dict"""
        return {
            "id": self.component_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "content": {"rights_list": self.rights_list},
            "html": self.to_html()
        }

    def to_html(self) -> str:
        if not self.rights_list:
            return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content">
        <p style="color: #999;">Loading your location-specific rights...</p>
    </div>
</div>
"""

        rights_html = ""
        for right in self.rights_list:
            rights_html += f"""
    <div class="right-item">
        <h4>{right['title']}</h4>
        <p>{right['description']}</p>
        {f'<small>Source: {right["source"]}</small>' if right["source"] else ''}
    </div>
"""

        return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content">
        {rights_html}
    </div>
</div>
"""


class InformationComponent(DashboardComponent):
    """ROW 2: Smart guidance, warnings, and information"""

    def __init__(self):
        super().__init__("row_2_information", "Important Information")
        self.css_class = "component-full-width information-box"
        self.warnings = []
        self.guidance_items = []

    def add_warning(self, title: str, description: str, severity: str = "info"):
        """Add a warning or alert"""
        self.warnings.append({
            "title": title,
            "description": description,
            "severity": severity  # "info", "warning", "critical"
        })

    def add_guidance(self, title: str, description: str):
        """Add guidance item"""
        self.guidance_items.append({
            "title": title,
            "description": description
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to JSON-serializable dict"""
        return {
            "id": self.component_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "content": {
                "warnings": self.warnings,
                "guidance_items": self.guidance_items
            },
            "html": self.to_html()
        }

    def to_html(self) -> str:
        items_html = ""

        # Add warnings
        for warning in self.warnings:
            severity_class = f"severity-{warning['severity']}"
            items_html += f"""
    <div class="info-item {severity_class}">
        <h4>⚠️ {warning['title']}</h4>
        <p>{warning['description']}</p>
    </div>
"""

        # Add guidance
        for guidance in self.guidance_items:
            items_html += f"""
    <div class="info-item guidance">
        <h4>💡 {guidance['title']}</h4>
        <p>{guidance['description']}</p>
    </div>
"""

        if not items_html:
            items_html = '<p style="color: #999;">No active alerts or guidance at this time.</p>'

        return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content">
        {items_html}
    </div>
</div>
"""


class InputComponent(DashboardComponent):
    """ROW 3: Flexible input boxes that scale based on situation"""

    def __init__(self):
        super().__init__("row_3_input", "Your Situation")
        self.css_class = "component-full-width input-box"
        self.input_fields = []

    def add_field(self, field_id: str, label: str, field_type: str = "text",
                 placeholder: str = "", required: bool = False, options: List[str] = None):
        """Add an input field"""
        self.input_fields.append({
            "id": field_id,
            "label": label,
            "type": field_type,
            "placeholder": placeholder,
            "required": required,
            "options": options or []
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to JSON-serializable dict"""
        return {
            "id": self.component_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "content": {"input_fields": self.input_fields},
            "html": self.to_html()
        }
    
    def to_html(self) -> str:
        if not self.input_fields:
            return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content">
        <p style="color: #999;">No input needed at this time.</p>
    </div>
</div>
"""

        fields_html = ""
        for field in self.input_fields:
            required_attr = "required" if field["required"] else ""

            if field["type"] == "select":
                options_html = "\n".join([f'<option value="{opt}">{opt}</option>' for opt in field["options"]])
                fields_html += f"""
    <div class="form-group">
        <label for="{field['id']}">{field['label']}</label>
        <select id="{field['id']}" name="{field['id']}" {required_attr}>
            <option value="">-- Select --</option>
            {options_html}
        </select>
    </div>
"""
            elif field["type"] == "textarea":
                fields_html += f"""
    <div class="form-group">
        <label for="{field['id']}">{field['label']}</label>
        <textarea id="{field['id']}" name="{field['id']}" placeholder="{field['placeholder']}" {required_attr}></textarea>
    </div>
"""
            elif field["type"] == "checkbox":
                fields_html += f"""
    <div class="form-group checkbox">
        <input type="checkbox" id="{field['id']}" name="{field['id']}" />
        <label for="{field['id']}">{field['label']}</label>
    </div>
"""
            else:  # text, email, phone, date, etc
                fields_html += f"""
    <div class="form-group">
        <label for="{field['id']}">{field['label']}</label>
        <input type="{field['type']}" id="{field['id']}" name="{field['id']}"
               placeholder="{field['placeholder']}" {required_attr} />
    </div>
"""

        return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <form class="component-form">
        <div class="component-content">
            {fields_html}
        </div>
        <button type="submit" class="btn btn-primary">Update My Situation</button>
    </form>
</div>
"""


class NextStepsComponent(DashboardComponent):
    """ROW 4: Action recommendations and next steps"""

    def __init__(self):
        super().__init__("row_4_next_steps", "Next Steps")
        self.css_class = "component-full-width next-steps-box"
        self.steps = []

    def add_step(self, step_number: int, title: str, description: str,
                 action_url: str = "", action_text: str = ""):
        """Add a next step"""
        self.steps.append({
            "number": step_number,
            "title": title,
            "description": description,
            "action_url": action_url,
            "action_text": action_text or "Learn More"
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to JSON-serializable dict"""
        return {
            "id": self.component_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "content": {"steps": self.steps},
            "html": self.to_html()
        }

    def to_html(self) -> str:
        if not self.steps:
            return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content">
        <p style="color: #999;">No recommended next steps at this time.</p>
    </div>
</div>
"""

        steps_html = ""
        for step in sorted(self.steps, key=lambda x: x["number"]):
            action_html = ""
            if step["action_url"]:
                action_html = f'<a href="{step["action_url"]}" class="btn btn-sm btn-secondary">{step["action_text"]}</a>'

            steps_html += f"""
    <div class="step-item">
        <div class="step-number">{step["number"]}</div>
        <div class="step-content">
            <h4>{step['title']}</h4>
            <p>{step['description']}</p>
            {action_html}
        </div>
    </div>
"""

        return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content steps-list">
        {steps_html}
    </div>
</div>
"""


class TimelineComponent(DashboardComponent):
    """ROW 5: Combined calendar dates and financial/ledger tracking timeline"""

    def __init__(self):
        super().__init__("row_5_timeline", "Important Dates & Timeline")
        self.css_class = "component-full-width timeline-box"
        self.timeline_items = []

    def add_event(self, event_date: str, title: str, description: str,
                 event_type: str = "deadline", related_amount: str = ""):
        """Add an event to timeline"""
        self.timeline_items.append({
            "date": event_date,
            "title": title,
            "description": description,
            "type": event_type,  # "deadline", "payment", "hearing", "document", "note"
            "amount": related_amount
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to JSON-serializable dict"""
        return {
            "id": self.component_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "content": {"timeline_items": self.timeline_items},
            "html": self.to_html()
        }

    def to_html(self) -> str:
        if not self.timeline_items:
            return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content">
        <p style="color: #999;">No upcoming dates at this time.</p>
    </div>
</div>
"""

        # Sort by date
        sorted_items = sorted(self.timeline_items, key=lambda x: x["date"])

        timeline_html = ""
        for item in sorted_items:
            type_icon = {
                "deadline": "📅",
                "payment": "💰",
                "hearing": "⚖️",
                "document": "📄",
                "note": "📝"
            }.get(item["type"], "•")

            amount_html = f'<p class="timeline-amount">{item["amount"]}</p>' if item["amount"] else ""

            timeline_html += f"""
    <div class="timeline-item">
        <div class="timeline-marker {item['type']}"></div>
        <div class="timeline-content">
            <p class="timeline-date">{type_icon} {item['date']}</p>
            <h4>{item['title']}</h4>
            <p>{item['description']}</p>
            {amount_html}
        </div>
    </div>
"""

        return f"""
<div class="{self.css_class}">
    <h2>{self.title}</h2>
    <div class="component-content timeline">
        {timeline_html}
    </div>
</div>
"""


class DashboardBuilder:
    """Builds complete dashboard from components"""

    def __init__(self):
        self.components = {}  # {row: component}
        self.rows = []

    def add_component(self, component: DashboardComponent, row: int):
        """Add component to dashboard at specific row"""
        self.components[component.component_id] = (row, component)
        if row not in self.rows:
            self.rows.append(row)
        self.rows.sort()

    def get_html(self) -> str:
        """Generate complete dashboard HTML"""
        html = '<div class="dashboard-container">\n'

        # Row 1: Rights
        if "row_1_rights" in self.components:
            html += self.components["row_1_rights"][1].to_html() + "\n"

        # Row 2: Information
        if "row_2_information" in self.components:
            html += self.components["row_2_information"][1].to_html() + "\n"

        # Row 3: Input (flexible)
        if "row_3_input" in self.components:
            html += self.components["row_3_input"][1].to_html() + "\n"

        # Row 4: Next Steps
        if "row_4_next_steps" in self.components:
            html += self.components["row_4_next_steps"][1].to_html() + "\n"

        # Row 5: Timeline
        if "row_5_timeline" in self.components:
            html += self.components["row_5_timeline"][1].to_html() + "\n"

        html += '</div>'
        return html

    def to_json(self) -> Dict[str, Any]:
        """Convert dashboard to JSON"""
        components_list = []
        for comp_id, (row_num, comp) in self.components.items():
            components_list.append({
                "row": row_num,
                "component": comp.to_dict()
            })
        return {
            "rows": self.rows,
            "components": components_list
        }
