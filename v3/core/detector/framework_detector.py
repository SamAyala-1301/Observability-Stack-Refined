"""Main framework detection orchestrator - ENHANCED VERSION."""
import docker
from typing import Optional, Dict
from .base import Detector, DetectionResult, Framework, Language
from .scanners.port_scanner import PortScanner
from .scanners.process_scanner import ProcessScanner
from .scanners.http_prober import HTTPProber
from .analyzers.env_analyzer import EnvAnalyzer
from .analyzers.file_analyzer import FileAnalyzer
from .analyzers.package_analyzer import PackageAnalyzer

class FrameworkDetector(Detector):
    """
    Enhanced orchestrator using multiple detection strategies.
    Combines: ports, processes, HTTP probes, env vars, files, packages.
    """
    
    def __init__(self):
        self.docker_client = docker.from_env()
        
        # Initialize all detectors
        self.port_scanner = PortScanner()
        self.process_scanner = ProcessScanner()
        self.http_prober = HTTPProber()
        self.env_analyzer = EnvAnalyzer()
        self.file_analyzer = FileAnalyzer()
        self.package_analyzer = PackageAnalyzer()
    
    def detect(self, container_id: str) -> DetectionResult:
        """
        Detect framework using ALL available strategies.
        Returns high-confidence result with detailed metadata.
        """
        try:
            container = self.docker_client.containers.get(container_id)
            container_name = container.name
            
            print(f"🔍 Scanning container: {container_name}")
            
            # Run ALL detection strategies
            print("  ├─ Port scanning...")
            port_hints = self.port_scanner.scan(container)
            
            print("  ├─ Process analysis...")
            process_hints = self.process_scanner.scan(container)
            
            print("  ├─ HTTP probing...")
            http_hints = self.http_prober.probe(container)
            
            print("  ├─ Environment variables...")
            env_hints = self.env_analyzer.analyze(container)
            
            print("  ├─ File system...")
            file_hints = self.file_analyzer.analyze(container)
            
            print("  └─ Package analysis...")
            package_hints = self.package_analyzer.analyze(container)
            
            # Combine all results with weighted scoring
            framework, language, confidence, version = self._combine_results(
                port_hints, 
                process_hints,
                http_hints,
                env_hints, 
                file_hints,
                package_hints
            )
            
            return DetectionResult(
                container_id=container_id,
                container_name=container_name,
                framework=framework,
                language=language,
                version=version,
                confidence=confidence,
                metadata={
                    "port_hints": port_hints,
                    "process_hints": process_hints,
                    "http_hints": http_hints,
                    "env_hints": env_hints,
                    "file_hints": file_hints,
                    "package_hints": package_hints
                }
            )
            
        except docker.errors.NotFound:
            raise ValueError(f"Container {container_id} not found")
        except Exception as e:
            raise RuntimeError(f"Detection failed: {e}")
    
    def _combine_results(self, port_hints, process_hints, http_hints, 
                        env_hints, file_hints, package_hints):
        """
        Combine all detection results with weighted scoring.
        
        Weights (total = 1.0):
        - Package analysis: 0.30 (most reliable)
        - Process scanning: 0.25 (very reliable)
        - File analysis: 0.20
        - HTTP probing: 0.15
        - Environment vars: 0.07
        - Port scanning: 0.03 (least reliable)
        """
        scores = {}
        version_hints = {}
        
        # Weight configuration
        weights = {
            "package": 0.30,
            "process": 0.25,
            "file": 0.20,
            "http": 0.15,
            "env": 0.07,
            "port": 0.03
        }
        
        # Aggregate scores from all sources
        for hint_type, hints, weight in [
            ("package", package_hints, weights["package"]),
            ("process", process_hints, weights["process"]),
            ("file", file_hints, weights["file"]),
            ("http", http_hints, weights["http"]),
            ("env", env_hints, weights["env"]),
            ("port", port_hints, weights["port"])
        ]:
            for key, score in hints.items():
                # Check if this is a version hint
                if isinstance(key, str) and '_version' in key:
                    framework_name = key.replace('_version', '')
                    version_hints[framework_name] = score
                elif isinstance(key, Framework):
                    if key not in scores:
                        scores[key] = 0
                    scores[key] += score * weight
        
        if not scores:
            return Framework.UNKNOWN, Language.UNKNOWN, 0.0, None
        
        # Get highest scoring framework
        best_framework = max(scores, key=scores.get)
        confidence = min(scores[best_framework], 1.0)  # Cap at 1.0
        
        # Get version if available
        version = version_hints.get(best_framework.value, None)
        
        # Map framework to language
        language_map = {
            Framework.FLASK: Language.PYTHON,
            Framework.DJANGO: Language.PYTHON,
            Framework.FASTAPI: Language.PYTHON,
            Framework.EXPRESS: Language.NODEJS,
            Framework.NESTJS: Language.NODEJS,
            Framework.SPRING_BOOT: Language.JAVA,
        }
        
        language = language_map.get(best_framework, Language.UNKNOWN)
        
        return best_framework, language, confidence, version
    
    def get_indicators(self) -> dict:
        """Get all detection indicators from all modules."""
        return {
            "port_indicators": self.port_scanner.get_indicators(),
            "process_indicators": self.process_scanner.get_indicators(),
            "http_indicators": self.http_prober.get_indicators(),
            "env_indicators": self.env_analyzer.get_indicators(),
            "file_indicators": self.file_analyzer.get_indicators(),
            "package_indicators": self.package_analyzer.get_indicators()
        }