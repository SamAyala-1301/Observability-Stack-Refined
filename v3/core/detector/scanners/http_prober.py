"""HTTP probing for framework fingerprinting."""
import requests
from typing import Optional, Tuple
from ..base import Framework

class HTTPProber:
    """Probe containers via HTTP to detect frameworks."""
    
    HEADER_PATTERNS = {
        'Server': {
            'Werkzeug': Framework.FLASK,
            'gunicorn': Framework.FLASK,
            'uvicorn': Framework.FASTAPI,
        },
        'X-Powered-By': {
            'Express': Framework.EXPRESS,
            'PHP': Framework.UNKNOWN,
        }
    }
    
    ENDPOINT_PATTERNS = {
        '/admin/': Framework.DJANGO,
        '/swagger/': Framework.SPRING_BOOT,
        '/docs': Framework.FASTAPI,
        '/actuator/': Framework.SPRING_BOOT,
    }
    
    def probe(self, container) -> dict:
        """
        Probe container HTTP endpoints.
        Returns framework hints based on HTTP responses.
        """
        hints = {}
        
        try:
            # Get container's IP address
            container_ip = self._get_container_ip(container)
            if not container_ip:
                return hints
            
            # Get exposed ports
            ports = self._get_exposed_ports(container)
            
            for port in ports:
                try:
                    # Try HTTP probe
                    response = requests.get(
                        f"http://{container_ip}:{port}",
                        timeout=3,
                        allow_redirects=False
                    )
                    
                    # Analyze headers
                    header_hints = self._analyze_headers(response.headers)
                    for framework, score in header_hints.items():
                        hints[framework] = hints.get(framework, 0) + score
                    
                    # Check common endpoints
                    endpoint_hints = self._probe_endpoints(container_ip, port)
                    for framework, score in endpoint_hints.items():
                        hints[framework] = hints.get(framework, 0) + score
                    
                except requests.exceptions.RequestException:
                    continue
        
        except Exception as e:
            print(f"HTTP probe error: {e}")
        
        return hints
    
    def _get_container_ip(self, container) -> Optional[str]:
        """Get container's IP address."""
        try:
            networks = container.attrs['NetworkSettings']['Networks']
            for network in networks.values():
                if network.get('IPAddress'):
                    return network['IPAddress']
        except Exception:
            pass
        return None
    
    def _get_exposed_ports(self, container) -> list:
        """Get list of exposed ports."""
        ports = []
        try:
            port_bindings = container.attrs.get('NetworkSettings', {}).get('Ports', {})
            for port_key in port_bindings.keys():
                port_num = int(port_key.split('/')[0])
                ports.append(port_num)
        except Exception:
            # Default common ports
            ports = [80, 8000, 8080, 5000, 3000, 4000]
        
        return ports[:5]  # Limit to 5 ports to avoid excessive probing
    
    def _analyze_headers(self, headers) -> dict:
        """Analyze HTTP headers for framework hints."""
        hints = {}
        
        for header_name, patterns in self.HEADER_PATTERNS.items():
            header_value = headers.get(header_name, '')
            
            for pattern, framework in patterns.items():
                if pattern.lower() in header_value.lower():
                    hints[framework] = 0.5
        
        return hints
    
    def _probe_endpoints(self, ip: str, port: int) -> dict:
        """Probe common framework-specific endpoints."""
        hints = {}
        
        for endpoint, framework in self.ENDPOINT_PATTERNS.items():
            try:
                response = requests.get(
                    f"http://{ip}:{port}{endpoint}",
                    timeout=2,
                    allow_redirects=False
                )
                
                # If endpoint exists (not 404), it's a hint
                if response.status_code != 404:
                    hints[framework] = hints.get(framework, 0) + 0.4
                    
            except requests.exceptions.RequestException:
                continue
        
        return hints
    
    def get_indicators(self) -> dict:
        """Get HTTP probing indicators."""
        return {
            "header_patterns": self.HEADER_PATTERNS,
            "endpoint_patterns": self.ENDPOINT_PATTERNS
        }