"""Bucket Interface & Seed Growth Manager
Writes generated engines to user's bucket, loads and executes them.
"""
from pathlib import Path
import importlib.util
import sys
from typing import Optional, Dict, Any
from seed_core import SeedCore, SeedGrowthEngine, SeedCapability
from datetime import datetime

class UserBucketSimulator:
    """Simulates user's R2/Google bucket for testing."""
    
    def __init__(self, bucket_path: str = "simulated_buckets/user_default"):
        self.bucket_path = Path(bucket_path)
        self.bucket_path.mkdir(parents=True, exist_ok=True)
        self.seed_dir = self.bucket_path / "semptify-seed"
        self.seed_dir.mkdir(exist_ok=True)
        (self.seed_dir / "engines").mkdir(exist_ok=True)
        (self.seed_dir / "data").mkdir(exist_ok=True)
        (self.seed_dir / "generated").mkdir(exist_ok=True)
    
    def write_file(self, path: str, content: str):
        """Write file to bucket."""
        file_path = self.seed_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
    
    def read_file(self, path: str) -> Optional[str]:
        """Read file from bucket."""
        file_path = self.seed_dir / path
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return None
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists in bucket."""
        return (self.seed_dir / path).exists()
    
    def list_files(self, prefix: str = "") -> list:
        """List files in bucket."""
        if prefix:
            search_path = self.seed_dir / prefix
        else:
            search_path = self.seed_dir
        return [str(p.relative_to(self.seed_dir)) for p in search_path.rglob('*') if p.is_file()]

class SeedManager:
    """Manages seed lifecycle: plant, grow, execute."""
    
    def __init__(self, bucket: UserBucketSimulator):
        self.bucket = bucket
        self.seed: Optional[SeedCore] = None
    
    def ensure_seed_exists(self, user_context: Dict[str, Any] = None):
        """Plant seed if doesn't exist, otherwise load it."""
        if self.bucket.file_exists("seed_core.json"):
            # Load existing seed
            seed_json = self.bucket.read_file("seed_core.json")
            self.seed = SeedCore.from_json(seed_json)
            print(f"📖 Loaded existing seed: {self.seed.seed_id}")
            print(f"   Capabilities: {len(self.seed.capabilities)}")
            print(f"   Interactions: {self.seed.interaction_count}")
        else:
            # Plant new seed
            self.seed = SeedCore.plant_new_seed(user_context)
            self._save_seed()
            print(f"🌱 Planted new seed: {self.seed.seed_id}")
    
    def _save_seed(self):
        """Save seed back to bucket."""
        self.bucket.write_file("seed_core.json", self.seed.to_json())
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input - grow engine if needed, execute it."""
        growth_engine = SeedGrowthEngine(self.seed)
        
        # Analyze what capability is needed
        needed_capability = growth_engine.analyze_need(user_input)
        
        if not needed_capability:
            return {
                'status': 'unclear',
                'message': 'Could not determine what you need. Can you be more specific?',
                'suggestion': 'Try describing your legal issue (eviction, rent, repairs, etc.)'
            }
        
        print(f"🔍 Detected need: {needed_capability}")
        
        # Check if seed has this capability
        if not self.seed.has_capability(needed_capability):
            print(f"🌱 Seed growing new capability: {needed_capability}")
            
            # Generate engine code
            engine_code = growth_engine.generate_engine_code(needed_capability)
            engine_filename = f"{needed_capability}.py"
            
            # Write to bucket
            self.bucket.write_file(f"engines/{engine_filename}", engine_code)
            
            # Add capability to seed
            capability = SeedCapability(
                name=needed_capability,
                engine_file=engine_filename,
                description=f"Generated from: {user_input[:50]}...",
                learned_from=user_input,
                created_at=datetime.utcnow().isoformat()
            )
            self.seed.add_capability(capability)
            self.seed.record_interaction(needed_capability)
            self._save_seed()
            
            print(f"✓ Engine written to bucket: engines/{engine_filename}")
        else:
            print(f"✓ Using existing capability: {needed_capability}")
        
        # Execute the engine
        result = self._execute_engine(needed_capability, user_input)
        
        # Update stats
        success = result.get('status') != 'error'
        self.seed.update_capability_stats(needed_capability, success)
        self._save_seed()
        
        return result
    
    def _execute_engine(self, capability_name: str, user_input: str) -> Dict[str, Any]:
        """Load and execute engine from bucket."""
        # Find engine file
        capability = next((c for c in self.seed.capabilities if c.name == capability_name), None)
        if not capability:
            return {'status': 'error', 'message': 'Capability not found'}
        
        engine_path = self.bucket.seed_dir / "engines" / capability.engine_file
        
        if not engine_path.exists():
            return {'status': 'error', 'message': f'Engine file not found: {capability.engine_file}'}
        
        # Dynamically load engine module
        spec = importlib.util.spec_from_file_location(capability_name, engine_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[capability_name] = module
        spec.loader.exec_module(module)
        
        # Execute based on capability type
        try:
            if capability_name == 'eviction_defense':
                result = module.analyze_eviction_notice(user_input, 'CA')
            elif capability_name == 'rent_calculator':
                result = module.calculate_rent_increase_legality(1500, 1800, 'CA', 2025)
            elif capability_name == 'motion_writer':
                result = module.generate_motion('continuance', {'case_number': 'ABC123', 'hearing_date': '2025-12-01'})
            else:
                result = {'status': 'processed', 'capability': capability_name}
            
            return {
                'status': 'success',
                'capability': capability_name,
                'result': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'capability': capability_name,
                'error': str(e)
            }
