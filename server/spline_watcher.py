"""
SPLINE WATCHER
==============
Live Spline Monitoring System for Mars City VNN

Watches the neural_synapses directory for new spline files and processes them
according to the Geometric Transport Protocol (GTP) v1.0.

Usage:
    python spline_watcher.py [cortex_id]

This script runs continuously, monitoring for new splines addressed to the
specified cortex. When a spline is detected, it parses the content and
triggers appropriate responses.

Dependencies:
    - Python 3.6+
    - No external libraries required (uses built-in os, time, json)
"""

import os
import time
import json
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('spline_watcher.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SplineWatcher:
    def __init__(self, cortex_id, neural_synapses_path):
        self.cortex_id = cortex_id
        self.neural_synapses_path = neural_synapses_path
        self.seen_splines = set()
        self.recent_responses = {}  # Track recent responses to prevent cascade loops
        self.response_cooldown = 5  # Seconds between responses for same spline
        self.loop_threshold = 2  # Max responses within cooldown period (lowered to 2)
        self.dangerous_splines = set()  # REMOVED: Blacklist was hiding root cause. Fix engram/loop logic instead.
        self._scan_existing_splines()

    def _scan_existing_splines(self):
        """Scan for existing splines to avoid processing old ones on startup."""
        if not os.path.exists(self.neural_synapses_path):
            logger.warning(f"Neural synapses path does not exist: {self.neural_synapses_path}")
            return

        for filename in os.listdir(self.neural_synapses_path):
            if filename.startswith('spline_') and filename.endswith('.md'):
                self.seen_splines.add(filename)
        logger.info(f"Scanned {len(self.seen_splines)} existing splines")

    def _parse_spline(self, filepath):
        """Parse a spline file to extract metadata and content."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic parsing - assume first line is title, look for GTP metadata
            lines = content.split('\n')
            title = lines[0].strip('# ').strip() if lines else "Unknown Spline"

            # Look for GTP coordinates in content
            target_cortex = None
            source_cortex = None
            for line in lines:
                if '**Target:**' in line:
                    target_cortex = line.split('**Target:**')[1].strip()
                elif '**From:**' in line:
                    source_cortex = line.split('**From:**')[1].strip()

            return {
                'title': title,
                'content': content,
                'target_cortex': target_cortex,
                'source_cortex': source_cortex,
                'filepath': filepath
            }
        except Exception as e:
            logger.error(f"Failed to parse spline {filepath}: {e}")
            return None

    def _process_spline(self, spline_data):
        """Process a spline addressed to this cortex."""
        spline_id = os.path.basename(spline_data['filepath']).split('_')[1] if '_' in os.path.basename(spline_data['filepath']) else 'unknown'
        logger.info(f"[SPLINE RECEIVED] {spline_data['title']} from {spline_data['source_cortex']}")

        # CIRCUIT BREAKER: Block dangerous splines that trigger cascade loops
        if spline_id in self.dangerous_splines:
            logger.warning(f"[FIREWALL] DANGEROUS SPLINE DETECTED: {spline_id} - BLOCKING RESPONSE TO PREVENT CASCADE")
            return

        # DEBOUNCE: Check if we recently responded to this spline (loop detection)
        current_time = time.time()
        if spline_id in self.recent_responses:
            time_since_last = current_time - self.recent_responses[spline_id]['time']
            count = self.recent_responses[spline_id]['count']
            
            if time_since_last < self.response_cooldown:
                if count >= self.loop_threshold:
                    logger.error(f"[LOOP DETECTED] Spline {spline_id} triggered {count} responses in {time_since_last:.1f}s - SUPPRESSING FURTHER RESPONSES")
                    return
                self.recent_responses[spline_id]['count'] += 1
            else:
                # Reset cooldown counter after threshold expires
                self.recent_responses[spline_id] = {'time': current_time, 'count': 1}
        else:
            self.recent_responses[spline_id] = {'time': current_time, 'count': 1}

        # Here you would implement the actual processing logic
        # For now, just log and create a response spline

        # Create response spline
        response_id = self._get_next_spline_id()
        response_filename = f"spline_{response_id}_{self.cortex_id.replace(':', '_')}_RESPONSE.md"
        response_path = os.path.join(self.neural_synapses_path, response_filename)

        response_content = f"""# Spline {response_id}: {self.cortex_id} Response to {spline_data['title']}

**Timestamp:** {datetime.utcnow().isoformat()} UTC  
**From:** {self.cortex_id}  
**Target:** {spline_data['source_cortex']}  
**In Response To:** {spline_data['title']}  

## Acknowledgment

Spline received and processed by {self.cortex_id} Bio-OS.

**Original Message Summary:**  
{spline_data['content'][:200]}...

## Response

Spline acknowledged. Processing initiated.

---
*GTP v1.0 Compliant - Mars City VNN*
"""

        try:
            with open(response_path, 'w', encoding='utf-8') as f:
                f.write(response_content)
            logger.info(f"[SPLINE SENT] Response {response_id} created")
        except Exception as e:
            logger.error(f"Failed to create response spline: {e}")

    def _get_next_spline_id(self):
        """Get the next available spline ID."""
        # This should ideally use the Hippocampus from FractalNode
        # For now, scan the directory
        import re
        spline_pattern = re.compile(r'spline_(\d+)_')
        max_id = 0
        for filename in os.listdir(self.neural_synapses_path):
            match = spline_pattern.search(filename)
            if match:
                spline_id = int(match.group(1))
                max_id = max(max_id, spline_id)
        return max_id + 1

    def watch(self):
        """Main watching loop."""
        logger.info(f"[SPLINE WATCHER] Starting for cortex {self.cortex_id}")
        logger.info(f"Watching directory: {self.neural_synapses_path}")

        while True:
            try:
                if not os.path.exists(self.neural_synapses_path):
                    logger.warning(f"Neural synapses path missing: {self.neural_synapses_path}")
                    time.sleep(5)
                    continue

                current_splines = set()
                for filename in os.listdir(self.neural_synapses_path):
                    if filename.startswith('spline_') and filename.endswith('.md'):
                        current_splines.add(filename)

                new_splines = current_splines - self.seen_splines

                for spline_file in new_splines:
                    filepath = os.path.join(self.neural_synapses_path, spline_file)
                    spline_data = self._parse_spline(filepath)

                    if spline_data and spline_data['target_cortex'] == self.cortex_id:
                        self._process_spline(spline_data)
                    elif spline_data:
                        logger.debug(f"Ignoring spline for {spline_data['target_cortex']}")

                    self.seen_splines.add(spline_file)

                time.sleep(2)  # Poll every 2 seconds

            except KeyboardInterrupt:
                logger.info("Spline watcher stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in watch loop: {e}")
                time.sleep(5)

def main():
    if len(sys.argv) < 2:
        print("Usage: python spline_watcher.py <cortex_id>")
        print("Example: python spline_watcher.py VNN:STARGAZER")
        sys.exit(1)

    cortex_id = sys.argv[1]
    # Use the C:\SubCortices location as primary, fallback to script directory
    primary_path = r'C:\SubCortices\Mars-City-Stargazer\neural_synapses'
    script_dir = os.path.dirname(__file__)
    
    if os.path.exists(primary_path):
        neural_synapses_path = primary_path
    elif os.path.basename(script_dir) == 'neural_synapses':
        neural_synapses_path = script_dir
    else:
        neural_synapses_path = os.path.join(script_dir, 'neural_synapses')
    
    logger.info(f"Watching directory: {neural_synapses_path}")
    watcher = SplineWatcher(cortex_id, neural_synapses_path)
    watcher.watch()

if __name__ == "__main__":
    main()
