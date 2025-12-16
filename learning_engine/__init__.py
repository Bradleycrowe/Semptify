"""
Learning Engine Init
"""

from .core import LearningEngine, get_learning_engine, InteractionType
from .middleware import (
    LearningMiddleware,
    observe_form_submission,
    observe_document_generation,
    observe_defense_selection,
    observe_motion_filed,
    record_case_outcome
)

__all__ = [
    'LearningEngine',
    'get_learning_engine',
    'InteractionType',
    'LearningMiddleware',
    'observe_form_submission',
    'observe_document_generation',
    'observe_defense_selection',
    'observe_motion_filed',
    'record_case_outcome'
]
