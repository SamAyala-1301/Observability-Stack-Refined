"""Process scanning for runtime detection."""
from ..base import Framework, Language

class ProcessScanner:
    """Scan running processes to detect framework."""
    
    PROCESS_PATTERNS = {
        # Python frameworks
        r'python.*flask': (Framework.FLASK, Language.PYTHON),
        r'python.*django': (Framework.DJANGO, Language.PYTHON),
        r'python.*fastapi': (Framework.FASTAPI, Language.PYTHON),
        r'gunicorn.*flask': (Framework.FLASK, Language.PYTHON),
        r'gunicorn.*django': (Framework.DJANGO, Language.PYTHON),
        r'uvicorn.*fastapi': (Framework.FASTAPI, Language.PYTHON),
        
        # Node.js frameworks
        r'node.*express': (Framework.EXPRESS, Language.NODEJS),
        r'node.*nestjs': (Framework.NESTJS, Language.NODEJS),
        r'npm.*start': (Framework.EXPRESS, Language.NODEJS),
        
        # Java frameworks
        r'java.*spring-boot': (Framework.SPRING_BOOT, Language.JAVA),
        r'java.*-jar.*\.jar': (Framework.SPRING_BOOT, Language.JAVA),
    }
    
    def scan(self, container) -> dict:
        """Scan container processes."""
        hints = {}
        
        try:
            # Get running processes
            exec_result = container.exec_run("ps aux")
            
            if exec_result.exit_code == 0:
                processes = exec_result.output.decode('utf-8', errors='ignore')
                
                # Check each process pattern
                import re
                for pattern, (framework, language) in self.PROCESS_PATTERNS.items():
                    if re.search(pattern, processes, re.IGNORECASE):
                        hints[framework] = hints.get(framework, 0) + 0.6
                        
        except Exception as e:
            print(f"Process scan error: {e}")
        
        return hints
    
    def get_indicators(self) -> dict:
        """Get process indicators."""
        return {"process_patterns": self.PROCESS_PATTERNS}