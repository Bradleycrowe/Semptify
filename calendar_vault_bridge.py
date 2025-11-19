"""
Calendar-Vault Bridge - ENHANCED Phase 2
Bidirectional sync: Events suggest uploads, uploads create events
"""
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict, Optional

class CalendarVaultBridge:
    '''Links calendar events to vault documents with intelligent bidirectional sync'''

    def __init__(self, vault_root='uploads/vault'):
        self.vault_root = vault_root
        # Common event types that should trigger document suggestions
        self.doc_trigger_events = {
            'repair_request': ['photos', 'correspondence'],
            'notice_received': ['notice_document', 'envelope_photo'],
            'inspection': ['photos', 'checklist'],
            'payment': ['receipt', 'proof_of_payment'],
            'complaint': ['complaint_document', 'evidence'],
            'move_in': ['lease', 'inspection_report', 'photos'],
            'move_out': ['final_inspection', 'photos', 'forwarding_address']
        }

    # ===== NEW: BIDIRECTIONAL SYNC =====
    
    def suggest_documents_for_event(self, event_type: str, event_data: dict) -> List[Dict]:
        '''
        When calendar event is created, suggest what documents user should upload
        
        Args:
            event_type: Type of event (repair_request, notice_received, etc.)
            event_data: Event details
            
        Returns:
            List of suggestions: [{doc_type, reason, urgency}]
        '''
        suggestions = []
        
        if event_type in self.doc_trigger_events:
            for doc_type in self.doc_trigger_events[event_type]:
                suggestions.append({
                    'doc_type': doc_type,
                    'reason': self._get_reason_for_doc(event_type, doc_type),
                    'urgency': self._get_urgency(event_type),
                    'event_id': event_data.get('event_id')
                })
        
        return suggestions
    
    def create_event_from_upload(self, user_id: str, document_info: dict) -> Optional[Dict]:
        '''
        When document is uploaded, auto-create calendar event if appropriate
        
        Args:
            user_id: User token
            document_info: {filename, file_type, upload_date, category}
            
        Returns:
            Event data if created, None otherwise
        '''
        filename = document_info.get('filename', '').lower()
        category = document_info.get('category', '').lower()
        
        # Detect event type from filename/category
        event_type = self._detect_event_type(filename, category)
        
        if event_type:
            event_data = {
                'event_id': f'evt_auto_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
                'title': self._generate_event_title(event_type, filename),
                'description': f'Automatically created from uploaded document: {document_info.get("filename")}',
                'event_date': document_info.get('upload_date', datetime.utcnow().isoformat()),
                'event_type': event_type,
                'auto_created': True,
                'source_document': document_info.get('doc_id')
            }
            
            # Link document to this event
            self.link_document_to_event(user_id, document_info.get('doc_id'), event_data['event_id'])
            
            return event_data
        
        return None
    
    def link_document_to_event(self, user_id: str, doc_id: str, event_id: str) -> bool:
        '''
        Link existing document to existing event
        
        Args:
            user_id: User token
            doc_id: Document ID
            event_id: Event ID
            
        Returns:
            True if linked successfully
        '''
        catalog_file = os.path.join(self.vault_root, f'user_{user_id}_catalog.json')
        
        entries = []
        if os.path.exists(catalog_file):
            with open(catalog_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)
        
        # Find the event and add document
        for entry in entries:
            if entry.get('event_id') == event_id:
                if 'documents' not in entry:
                    entry['documents'] = []
                if doc_id not in entry['documents']:
                    entry['documents'].append(doc_id)
                    
                    # Save updated catalog
                    with open(catalog_file, 'w', encoding='utf-8') as f:
                        json.dump(entries, f, indent=2)
                    return True
        
        return False
    
    def get_events_needing_documents(self, user_id: str) -> List[Dict]:
        '''
        Find calendar events that are missing suggested documents
        
        Returns:
            List of events with missing_docs: [{event, missing_docs: [doc_types]}]
        '''
        catalog_file = os.path.join(self.vault_root, f'user_{user_id}_catalog.json')
        
        if not os.path.exists(catalog_file):
            return []
        
        with open(catalog_file, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        
        needs_docs = []
        for entry in entries:
            event_type = entry.get('event_type')
            if event_type in self.doc_trigger_events:
                expected_docs = self.doc_trigger_events[event_type]
                actual_docs = entry.get('documents', [])
                
                if len(actual_docs) < len(expected_docs):
                    needs_docs.append({
                        'event': entry,
                        'missing_docs': [d for d in expected_docs if d not in [self._get_doc_type(doc) for doc in actual_docs]],
                        'urgency': self._calculate_event_urgency(entry)
                    })
        
        return needs_docs
    
    # ===== HELPER METHODS =====
    
    def _detect_event_type(self, filename: str, category: str) -> Optional[str]:
        '''Detect event type from filename/category'''
        keywords = {
            'repair': 'repair_request',
            'notice': 'notice_received',
            'eviction': 'notice_received',
            'lease': 'move_in',
            'receipt': 'payment',
            'inspection': 'inspection'
        }
        
        for keyword, event_type in keywords.items():
            if keyword in filename or keyword in category:
                return event_type
        
        return None
    
    def _generate_event_title(self, event_type: str, filename: str) -> str:
        '''Generate human-readable title for auto-created event'''
        titles = {
            'repair_request': f'Repair Issue - {filename[:30]}',
            'notice_received': f'Notice Received - {filename[:30]}',
            'payment': f'Payment Made - {filename[:30]}',
            'inspection': f'Inspection - {filename[:30]}',
            'move_in': f'Move-In Documentation - {filename[:30]}'
        }
        return titles.get(event_type, f'Document Event - {filename[:30]}')
    
    def _get_reason_for_doc(self, event_type: str, doc_type: str) -> str:
        '''Explain why this document is suggested'''
        reasons = {
            ('repair_request', 'photos'): 'Photos prove the condition before and after repair',
            ('repair_request', 'correspondence'): 'Written requests create a paper trail',
            ('notice_received', 'notice_document'): 'Original notice is critical evidence',
            ('notice_received', 'envelope_photo'): 'Envelope proves date received',
            ('payment', 'receipt'): 'Receipt proves payment was made',
            ('inspection', 'photos'): 'Photos document property condition',
            ('move_in', 'lease'): 'Lease is your primary contract',
            ('move_in', 'inspection_report'): 'Move-in condition protects your deposit'
        }
        return reasons.get((event_type, doc_type), f'Recommended for {event_type} events')
    
    def _get_urgency(self, event_type: str) -> str:
        '''Determine urgency level for document upload'''
        urgent_events = ['notice_received', 'eviction', 'complaint']
        return 'high' if event_type in urgent_events else 'normal'
    
    def _get_doc_type(self, doc_id: str) -> str:
        '''Extract document type from doc ID or metadata'''
        # Simplified - in real implementation, check document metadata
        return doc_id.split('_')[0] if '_' in doc_id else 'unknown'
    
    def _calculate_event_urgency(self, event: dict) -> str:
        '''Calculate current urgency based on event date and type'''
        event_date = event.get('event_date')
        if not event_date:
            return 'normal'
        
        try:
            evt_dt = datetime.fromisoformat(event_date)
            days_ago = (datetime.now() - evt_dt).days
            
            if days_ago < 7:
                return 'high'
            elif days_ago < 30:
                return 'medium'
            else:
                return 'normal'
        except:
            return 'normal'

    # ===== ORIGINAL METHODS (keep existing functionality) =====

    def catalog_event_with_documents(self, user_id: str, event_data: dict, document_ids: List[str]) -> dict:
        '''Catalog an event with its associated documents'''
        timestamp = datetime.utcnow().isoformat()
        catalog_entry = {
            'event_id': event_data.get('event_id', f'evt_{timestamp.replace(":", "").replace("-", "").replace(".", "")}'),
            'user_id': user_id,
            'timestamp': timestamp,
            'event_date': event_data.get('event_date'),
            'title': event_data.get('title'),
            'description': event_data.get('description'),
            'event_type': event_data.get('event_type', 'general'),
            'documents': [],
            'vault_paths': []
        }

        for doc_id in document_ids:
            doc_info = self._get_document_info(user_id, doc_id)
            if doc_info:
                catalog_entry['documents'].append(doc_id)
                catalog_entry['vault_paths'].append(doc_info['path'])

        self._save_catalog_entry(user_id, catalog_entry)
        return catalog_entry

    def get_chronological_view(self, user_id: str, view_type='day') -> List[Dict]:
        '''Get organized chronological view of events + documents'''
        catalog_file = os.path.join(self.vault_root, f'user_{user_id}_catalog.json')

        if not os.path.exists(catalog_file):
            return []

        with open(catalog_file, 'r', encoding='utf-8') as f:
            all_entries = json.load(f)

        sorted_entries = sorted(all_entries, key=lambda x: x['timestamp'], reverse=True)

        if view_type == 'day':
            return self._group_by_day(sorted_entries)
        elif view_type == 'week':
            return self._group_by_week(sorted_entries)
        elif view_type == 'month':
            return self._group_by_month(sorted_entries)
        elif view_type == 'year':
            return self._group_by_year(sorted_entries)

        return sorted_entries

    def _get_document_info(self, user_id: str, doc_id: str) -> dict:
        user_dir = os.path.join(self.vault_root, user_id)
        cert_file = os.path.join(user_dir, f'{doc_id}.cert.json')
        
        if os.path.exists(cert_file):
            with open(cert_file, 'r', encoding='utf-8') as f:
                cert = json.load(f)
            return {
                'doc_id': doc_id,
                'path': cert.get('file_path', ''),
                'sha256': cert.get('sha256', ''),
                'timestamp': cert.get('timestamp', cert.get('ts', ''))
            }
        return None

    def _save_catalog_entry(self, user_id: str, entry: dict):
        catalog_file = os.path.join(self.vault_root, f'user_{user_id}_catalog.json')

        entries = []
        if os.path.exists(catalog_file):
            with open(catalog_file, 'r', encoding='utf-8') as f:
                entries = json.load(f)

        entries.append(entry)

        with open(catalog_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2)

    def _group_by_day(self, entries: List[Dict]) -> List[Dict]:
        grouped = {}
        for entry in entries:
            date = entry['event_date'][:10] if entry.get('event_date') else entry['timestamp'][:10]
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(entry)
        return [{'date': k, 'events': v} for k, v in grouped.items()]

    def _group_by_week(self, entries: List[Dict]) -> List[Dict]:
        grouped = {}
        for entry in entries:
            dt = datetime.fromisoformat(entry['event_date'] if entry.get('event_date') else entry['timestamp'])
            week = f'{dt.year}-W{dt.isocalendar()[1]:02d}'
            if week not in grouped:
                grouped[week] = []
            grouped[week].append(entry)
        return [{'week': k, 'events': v} for k, v in grouped.items()]
    
    def _group_by_month(self, entries: List[Dict]) -> List[Dict]:
        grouped = {}
        for entry in entries:
            date = entry['event_date'][:7] if entry.get('event_date') else entry['timestamp'][:7]
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(entry)
        return [{'month': k, 'events': v} for k, v in grouped.items()]

    def _group_by_year(self, entries: List[Dict]) -> List[Dict]:
        grouped = {}
        for entry in entries:
            year = entry['event_date'][:4] if entry.get('event_date') else entry['timestamp'][:4]
            if year not in grouped:
                grouped[year] = []
            grouped[year].append(entry)
        return [{'year': k, 'events': v} for k, v in grouped.items()]