#!/usr/bin/env python3
"""
DDoS Attack Detection Script
Educational Purpose - Cybersecurity Defense
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict

class DDoSDetector:
    def __init__(self, threshold=100, window_minutes=5):
        self.threshold = threshold
        self.window = timedelta(minutes=window_minutes)
        self.connections = defaultdict(list)
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ddos_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('DDoSDetector')
    
    def monitor_connection(self, source_ip, target_port):
        """Monitor a new connection attempt"""
        timestamp = datetime.now()
        
        # Log the connection
        self.connections[target_port].append((source_ip, timestamp))
        
        # Clean old entries
        self.clean_old_entries()
        
        # Check for potential DDoS
        self.check_for_attacks(target_port)
    
    def clean_old_entries(self):
        """Remove connections older than detection window"""
        cutoff_time = datetime.now() - self.window
        
        for port in list(self.connections.keys()):
            self.connections[port] = [
                (ip, ts) for ip, ts in self.connections[port]
                if ts > cutoff_time
            ]
            
            # Remove empty port entries
            if not self.connections[port]:
                del self.connections[port]
    
    def check_for_attacks(self, target_port):
        """Check for DDoS patterns on specific port"""
        if target_port not in self.connections:
            return
        
        connections = self.connections[target_port]
        
        if len(connections) > self.threshold:
            unique_ips = len(set(ip for ip, ts in connections))
            
            self.logger.warning(
                f"🚨 POTENTIAL DDoS DETECTED - Port {target_port}: "
                f"{len(connections)} connections from {unique_ips} unique IPs"
            )
            
            # Generate alert details
            self.generate_alert(target_port, connections)
    
    def generate_alert(self, port, connections):
        """Generate detailed DDoS alert"""
        alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unique_ips = set(ip for ip, ts in connections)
        
        alert_message = f"""
        🚨 DDoS ALERT - {alert_time}
        Target Port: {port}
        Connections: {len(connections)}
        Unique IPs: {len(unique_ips)}
        First 5 IPs: {list(unique_ips)[:5]}
        """
        
        print(alert_message)
        self.logger.critical(alert_message)
    
    def get_statistics(self):
        """Get current monitoring statistics"""
        stats = {
            'total_ports_monitored': len(self.connections),
            'total_connections': sum(len(conns) for conns in self.connections.values()),
            'detection_threshold': self.threshold,
            'monitoring_window_minutes': self.window.total_seconds() / 60
        }
        return stats

def main():
    """Demo the DDoS detection system"""
    print("🔍 DDoS Detection System - Educational Demo")
    print("=" * 50)
    
    # Create detector
    detector = DDoSDetector(threshold=50, window_minutes=2)
    
    # Simulate normal traffic
    print("1. Simulating normal traffic...")
    for i in range(20):
        detector.monitor_connection(f"192.168.1.{i}", 80)
    
    print(f"Normal traffic stats: {detector.get_statistics()}")
    
    # Simulate DDoS attack
    print("\n2. Simulating DDoS attack on port 30120...")
    for i in range(100):
        detector.monitor_connection(f"10.0.0.{i % 30}", 30120)
    
    print(f"After attack simulation: {detector.get_statistics()}")
    
    print("\n3. Demo completed.")
    print("⚠️  This script is for educational purposes only!")

if __name__ == "__main__":
    main()