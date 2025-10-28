#!/usr/bin/env python3
"""
Continuous Monitoring Batch Job
Runs every 10 seconds via Kubernetes CronJob
"""
import logging
import psutil
import socket
from datetime import datetime
import os
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def get_system_metrics():
    """Collect comprehensive system metrics"""
    try:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "job_mode": os.getenv('JOB_MODE', 'default'),
            "cpu_usage": f"{psutil.cpu_percent(interval=1)}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "available_memory": f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            "disk_usage": f"{psutil.disk_usage('/').percent}%",
            "running_processes": len(psutil.pids()),
            "load_avg": os.getloadavg()
        }
        return metrics
    except Exception as e:
        return {"error": str(e)}

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Starting Continuous Monitoring Batch Job")
    
    try:
        # Collect metrics
        metrics = get_system_metrics()
        
        # Log all metrics
        logger.info("📊 System Metrics Collected:")
        for key, value in metrics.items():
            logger.info(f"   {key}: {value}")
        
        # Health check
        memory_usage = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=1)
        
        if memory_usage > 90 or cpu_usage > 90:
            logger.warning(f"🚨 High Resource Usage - CPU: {cpu_usage}%, Memory: {memory_usage}%")
        else:
            logger.info(f"✅ System Healthy - CPU: {cpu_usage}%, Memory: {memory_usage}%")
            
        logger.info("🎯 Monitoring cycle completed successfully")
        
    except Exception as e:
        logger.error(f"💥 Monitoring job failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()