"""
Performance monitoring and logging for Phase 6 hardening.
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

import psutil
import threading


class LogLevel(Enum):
    """Log levels for structured logging."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class PerformanceMetrics:
    """Performance metrics collection."""
    start_time: float
    end_time: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    cpu_usage_percent: Optional[float] = None
    api_calls: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    errors: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        data = asdict(self)
        if self.end_time:
            data["duration_ms"] = (self.end_time - self.start_time) * 1000
        return data


@dataclass
class APIMetrics:
    """API call metrics."""
    endpoint: str
    method: str
    response_time_ms: float
    success: bool
    status_code: Optional[int] = None
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None


class PerformanceMonitor:
    """Monitor system performance and API calls."""
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.api_metrics: list[APIMetrics] = []
        self.logger = self._setup_logger()
        self._lock = threading.Lock()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logger."""
        logger = logging.getLogger("phase6_monitoring")
        
        # Create handler for structured logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        return logger
    
    def start_operation(self, operation_name: str) -> str:
        """Start monitoring an operation."""
        operation_id = f"{operation_name}_{int(time.time())}"
        
        with self._lock:
            self.metrics[operation_id] = PerformanceMetrics(
                start_time=time.time(),
                memory_usage_mb=self._get_memory_usage(),
                cpu_usage_percent=self._get_cpu_usage()
            )
        
        self.logger.info(f"Started operation: {operation_name} (ID: {operation_id})")
        return operation_id
    
    def end_operation(self, operation_id: str, api_metrics: Optional[APIMetrics] = None) -> Dict[str, Any]:
        """End monitoring an operation."""
        with self._lock:
            if operation_id not in self.metrics:
                self.logger.warning(f"Operation ID not found: {operation_id}")
                return {}
            
            metrics = self.metrics[operation_id]
            metrics.end_time = time.time()
            metrics.memory_usage_mb = self._get_memory_usage()
            metrics.cpu_usage_percent = self._get_cpu_usage()
            
            if api_metrics:
                self.api_metrics.append(api_metrics)
                metrics.api_calls += 1
                if not api_metrics.success:
                    metrics.errors += 1
            
            result = metrics.to_dict()
            
            # Log completion
            log_data = {
                "operation_id": operation_id,
                "duration_ms": result.get("duration_ms"),
                "success": api_metrics.success if api_metrics else True,
                "memory_mb": result.get("memory_usage_mb"),
                "cpu_percent": result.get("cpu_usage_percent")
            }
            
            if api_metrics:
                log_data.update({
                    "api_endpoint": api_metrics.endpoint,
                    "status_code": api_metrics.status_code,
                    "response_time_ms": api_metrics.response_time_ms,
                    "tokens_used": api_metrics.tokens_used
                })
            
            self.logger.info(f"Completed operation: {operation_id}", extra=log_data)
            
            # Clean up old metrics (keep last 100)
            if len(self.metrics) > 100:
                old_keys = list(self.metrics.keys())[:-100]
                for old_key in old_keys:
                    del self.metrics[old_key]
            
            return result
    
    def log_api_call(self, endpoint: str, method: str, **kwargs):
        """Log an API call and return metrics object."""
        start_time = time.time()
        
        def complete_call(status_code: int, success: bool, error_message: str = None, tokens_used: int = None):
            response_time = (time.time() - start_time) * 1000
            
            metrics = APIMetrics(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                response_time_ms=response_time,
                tokens_used=tokens_used,
                success=success,
                error_message=error_message
            )
            
            self.logger.info(f"API call: {method} {endpoint}", extra={
                "status_code": status_code,
                "response_time_ms": response_time,
                "success": success,
                "tokens_used": tokens_used,
                "error_message": error_message
            })
            
            return metrics
        
        return complete_call
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return memory_info.rss / (1024 * 1024)  # Convert to MB
        except Exception:
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        try:
            return psutil.cpu_percent()
        except Exception:
            return 0.0
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for monitoring."""
        with self._lock:
            if not self.metrics:
                return {"message": "No operations recorded"}
            
            total_operations = len(self.metrics)
            total_errors = sum(m.errors for m in self.metrics.values())
            total_api_calls = sum(m.api_calls for m in self.metrics.values())
            
            # Calculate average duration
            completed_operations = [m for m in self.metrics.values() if m.end_time is not None]
            avg_duration = 0
            if completed_operations:
                durations = [(m.end_time - m.start_time) * 1000 for m in completed_operations]
                avg_duration = sum(durations) / len(durations)
            
            # API metrics summary
            successful_api_calls = len([m for m in self.api_metrics if m.success])
            failed_api_calls = len(self.api_metrics) - successful_api_calls
            
            return {
                "total_operations": total_operations,
                "total_errors": total_errors,
                "total_api_calls": total_api_calls,
                "successful_api_calls": successful_api_calls,
                "failed_api_calls": failed_api_calls,
                "average_duration_ms": round(avg_duration, 2),
                "current_memory_mb": self._get_memory_usage(),
                "current_cpu_percent": self._get_cpu_usage()
            }
    
    def export_metrics(self, filename: str) -> None:
        """Export metrics to JSON file."""
        try:
            summary = self.get_performance_summary()
            
            with open(filename, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "summary": summary,
                    "detailed_metrics": {k: v.to_dict() for k, v in self.metrics.items()},
                    "api_calls": [asdict(m) for m in self.api_metrics]
                }, f, indent=2)
            
            self.logger.info(f"Exported metrics to: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")


class LoggingConfig:
    """Configuration for structured logging."""
    
    def __init__(self, log_level: LogLevel = LogLevel.INFO):
        self.log_level = log_level
        self._configure_logging()
    
    def _configure_logging(self) -> None:
        """Configure logging with structured output."""
        logging.basicConfig(
            level=getattr(logging, self.log_level.value),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('phase6_monitoring.log')
            ]
        )
        
        # Configure third-party loggers
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("datasets").setLevel(logging.WARNING)
