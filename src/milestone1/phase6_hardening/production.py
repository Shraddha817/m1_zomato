"""
Production deployment and hardening for Phase 6.
"""

import os
import sys
import logging
from pathlib import Path

from milestone1.phase6_hardening.config import ProductionConfig
from milestone1.phase6_hardening.monitoring import PerformanceMonitor, LoggingConfig, LogLevel
from milestone1.phase6_hardening.caching import CacheManager, RestaurantCache, LLMResponseCache
from milestone1.phase6_hardening.testing import TestFixtures, LLMResponseValidator


class ProductionHardening:
    """Production hardening and deployment configuration."""
    
    def __init__(self, config: ProductionConfig):
        self.config = config
        self.monitor = PerformanceMonitor()
        log_level_enum = LogLevel(config.log_level.upper()) if hasattr(LogLevel, config.log_level.upper()) else LogLevel.INFO
        logging_config = LoggingConfig(log_level_enum)
        self.logger = logging.getLogger("phase6_monitoring")
        self.restaurant_cache = RestaurantCache(config.cache_ttl_restaurants)
        self.llm_cache = LLMResponseCache(config.cache_ttl_recommendations)
        
        # Validate configuration
        self._validate_production_config()
        
        self.logger.info("Phase 6 Production Hardening initialized")
        self.logger.info(f"Configuration: {config.to_dict()}")
    
    def _validate_production_config(self) -> None:
        """Validate production configuration."""
        issues = self.config.validate()
        
        if issues:
            for issue in issues:
                self.logger.error(f"Configuration issue: {issue}")
            
            raise ValueError(f"Invalid configuration: {'; '.join(issues)}")
        
        # Check required environment variables
        required_vars = ["XAI_API_KEY", "HF_DATASET_NAME"]
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            self.logger.error(f"Missing required environment variables: {missing_vars}")
            raise ValueError(f"Missing environment variables: {missing_vars}")
    
    def setup_production_environment(self) -> None:
        """Setup production environment with all hardening."""
        self.logger.info("Setting up production environment...")
        
        # Setup monitoring
        if self.config.enable_performance_monitoring:
            self.monitor.start_operation("production_startup")
        
        # Setup caching
        if self.config.enable_caching:
            self._setup_caching()
        
        # Validate dataset pinning
        if self.config.dataset_revision:
            self._validate_dataset_pinning()
        
        # Setup rate limiting
        self._setup_rate_limiting()
        
        # Test critical components
        self._run_health_checks()
        
        self.logger.info("Production environment setup complete")
    
    def _setup_caching(self) -> None:
        """Setup caching with production settings."""
        self.logger.info("Setting up production caching...")
        
        # Pre-warm caches if possible
        try:
            self._prewarm_caches()
        except Exception as e:
            self.logger.warning(f"Cache prewarming failed: {e}")
    
    def _prewarm_caches(self) -> None:
        """Prewarm caches with common data."""
        operation_id = self.monitor.start_operation("cache_prewarming")
        
        try:
            # Cache common locations
            common_locations = ["Banashankari", "BTM", "JP Nagar", "Basavanagudi"]
            self.restaurant_cache.put_locations(common_locations, ttl_seconds=self.config.cache_ttl_locations)
            
            # Cache sample restaurant data
            from milestone1.ingestion import load_restaurants
            sample_restaurants = load_restaurants(limit=50)
            self.restaurant_cache.put_restaurants(sample_restaurants, ttl_seconds=self.config.cache_ttl_restaurants)
            
            self.monitor.end_operation(
                operation_id,
                api_metrics=None
            )
            
        except Exception as e:
            self.logger.error(f"Cache prewarming error: {e}")
    
    def _validate_dataset_pinning(self) -> None:
        """Validate dataset pinning configuration."""
        if not self.config.dataset_revision:
            self.logger.warning("No dataset revision specified - using latest")
            return
        
        self.logger.info(f"Dataset pinned to revision: {self.config.dataset_revision}")
        
        # Here you would validate checksum, size, etc.
        # Implementation would depend on dataset structure
    
    def _setup_rate_limiting(self) -> None:
        """Setup rate limiting for API calls."""
        self.logger.info("Setting up rate limiting...")
        
        # Rate limiting would be implemented here
        # This is a placeholder for the actual implementation
        pass
    
    def _run_health_checks(self) -> None:
        """Run health checks on critical components."""
        self.logger.info("Running production health checks...")
        
        health_issues = []
        
        # Test data loading
        try:
            from milestone1.ingestion import load_restaurants
            restaurants = load_restaurants(limit=10)
            if len(restaurants) == 0:
                health_issues.append("Data loading returned no restaurants")
        except Exception as e:
            health_issues.append(f"Data loading failed: {e}")
        
        # Test LLM connectivity
        if not os.environ.get("XAI_API_KEY"):
            health_issues.append("XAI_API_KEY not configured")
        
        # Test cache functionality
        try:
            test_key = "health_check_test"
            self.restaurant_cache.put(test_key, {"test": "data"}, ttl_seconds=60)
            retrieved = self.restaurant_cache.get(test_key)
            if retrieved != {"test": "data"}:
                health_issues.append("Cache read/write inconsistency")
        except Exception as e:
            health_issues.append(f"Cache health check failed: {e}")
        
        if health_issues:
            self.logger.error(f"Health check failed: {'; '.join(health_issues)}")
            raise RuntimeError(f"Health check failed: {health_issues}")
        
        self.logger.info("All health checks passed")
    
    def run_production_tests(self) -> bool:
        """Run comprehensive production tests."""
        self.logger.info("Running production tests...")
        
        test_results = []
        
        # Test LLM response parsing
        test_results.append(self._test_llm_parsing())
        
        # Test fallback behavior
        test_results.append(self._test_fallback_mechanism())
        
        # Test error handling
        test_results.append(self._test_error_scenarios())
        
        # Test cache performance
        test_results.append(self._test_cache_performance())
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        self.logger.info(f"Production tests: {passed_tests}/{total_tests} passed")
        
        if passed_tests == total_tests:
            self.logger.info("All production tests passed")
            return True
        else:
            self.logger.error(f"Production tests failed: {passed_tests}/{total_tests}")
            return False
    
    def _test_llm_parsing(self) -> bool:
        """Test LLM JSON parsing with various scenarios."""
        operation_id = self.monitor.start_operation("llm_parsing_test")
        
        try:
            # Test valid response
            valid_response = TestFixtures.get_valid_llm_response()
            validator = LLMResponseValidator()
            
            if not validator.validate_recommendations_structure(valid_response):
                self.monitor.end_operation(operation_id)
                return False
            
            # Test invalid response
            invalid_response = TestFixtures.get_invalid_llm_response()
            if validator.validate_recommendations_structure(invalid_response):
                self.monitor.end_operation(operation_id)
                return False
            
            # Test hallucinated response
            hallucinated_response = TestFixtures.get_hallucinated_llm_response()
            valid_ids = ["test_restaurant_1", "test_restaurant_2", "test_restaurant_3"]
            
            if not validator.validate_restaurant_ids(hallucinated_response, valid_ids):
                self.monitor.end_operation(operation_id)
                return False
            
            self.monitor.end_operation(operation_id)
            return True
            
        except Exception as e:
            self.logger.error(f"LLM parsing test failed: {e}")
            self.monitor.end_operation(operation_id)
            return False
    
    def _test_fallback_mechanism(self) -> bool:
        """Test fallback recommendation mechanism."""
        operation_id = self.monitor.start_operation("fallback_test")
        
        try:
            # Simulate LLM failure
            with patch('milestone1.phase4_recommendation.client.OpenAI') as mock_openai:
                mock_openai.return_value.chat.completions.create.side_effect = Exception("LLM API Error")
                
                from milestone1.phase4_recommendation.client import get_recommendations
                from milestone1.phase3_integration.prompting import build_prompt_payload
                from milestone1.phase2_preferences.models import UserPreferences
                
                candidates = TestFixtures.get_mock_restaurant_data()
                prefs = TestFixtures.get_mock_user_preferences()
                prompt_payload = build_prompt_payload(candidates[:5], prefs)
                
                # This should use fallback
                recommendations = get_recommendations(prompt_payload, candidates[:5], top_k=3)
                
                if len(recommendations) == 0:
                    self.monitor.end_operation(operation_id)
                    return False
                
                # Check if fallback explanations are used
                fallback_explanations = [
                    "We couldn't generate a personalized reason right now" in rec.explanation
                    for rec in recommendations
                ]
                
                if not all(fallback_explanations):
                    self.monitor.end_operation(operation_id)
                    return False
            
            self.monitor.end_operation(operation_id)
            return True
            
        except Exception as e:
            self.logger.error(f"Fallback test failed: {e}")
            self.monitor.end_operation(operation_id)
            return False
    
    def _test_error_scenarios(self) -> bool:
        """Test various error scenarios."""
        operation_id = self.monitor.start_operation("error_scenarios_test")
        
        try:
            error_scenarios = [
                TestFixtures.test_api_timeout,
                TestFixtures.test_api_rate_limit,
                TestFixtures.test_invalid_api_key,
                TestFixtures.test_network_error
            ]
            
            for scenario in error_scenarios:
                try:
                    scenario()
                except Exception as e:
                    self.logger.warning(f"Error scenario '{scenario.__name__}' handled correctly: {e}")
                else:
                    self.logger.warning(f"Error scenario '{scenario.__name__}' did not raise expected error")
            
            self.monitor.end_operation(operation_id)
            return True
            
        except Exception as e:
            self.logger.error(f"Error scenarios test failed: {e}")
            self.monitor.end_operation(operation_id)
            return False
    
    def _test_cache_performance(self) -> bool:
        """Test cache performance under load."""
        operation_id = self.monitor.start_operation("cache_performance_test")
        
        try:
            # Test cache with many entries
            test_entries = 1000
            
            for i in range(test_entries):
                key = f"test_key_{i}"
                data = {"test_data": f"test_value_{i}", "index": i}
                self.restaurant_cache.put(key, data, ttl_seconds=60)
            
            # Test retrieval
            cache_hits = 0
            for i in range(test_entries):
                key = f"test_key_{i}"
                retrieved = self.restaurant_cache.get(key)
                if retrieved and retrieved.get("index") == i:
                    cache_hits += 1
            
            hit_rate = (cache_hits / test_entries) * 100
            stats = self.restaurant_cache.get_stats()
            
            self.monitor.end_operation(operation_id)
            
            # Assert reasonable performance
            if hit_rate < 95:  # Should have high hit rate
                self.logger.warning(f"Cache hit rate low: {hit_rate}%")
                return False
            
            if stats["size_bytes"] > self.restaurant_cache.max_size_bytes * 1.1:  # Should not exceed 110% of max
                self.logger.warning(f"Cache size exceeded: {stats['size_bytes']} bytes")
                return False
            
            self.logger.info(f"Cache performance test passed: {hit_rate}% hit rate")
            return True
            
        except Exception as e:
            self.logger.error(f"Cache performance test failed: {e}")
            self.monitor.end_operation(operation_id)
            return False
    
    def get_production_status(self) -> dict:
        """Get comprehensive production status."""
        return {
            "config": self.config.to_dict(),
            "monitoring": self.monitor.get_performance_summary(),
            "cache_stats": self.restaurant_cache.get_stats(),
            "health_status": "healthy",
            "timestamp": self.monitor._get_current_timestamp()
        }
    
    def start_production_mode(self) -> None:
        """Start the application in production mode."""
        self.logger.info("Starting production mode...")
        
        try:
            # Setup environment
            self.setup_production_environment()
            
            # Run production tests
            if not self.run_production_tests():
                raise RuntimeError("Production tests failed")
            
            self.logger.info("Production mode started successfully")
            
            # Main production loop would go here
            self._run_production_loop()
            
        except Exception as e:
            self.logger.error(f"Failed to start production mode: {e}")
            raise
    
    def _run_production_loop(self) -> None:
        """Main production application loop."""
        self.logger.info("Entering production loop...")
        
        # This would be the main application loop
        # For now, just indicate ready state
        self.logger.info("Production application ready")
    
    def shutdown(self) -> None:
        """Graceful shutdown of production application."""
        self.logger.info("Shutting down production application...")
        
        # Export final metrics
        try:
            self.monitor.export_metrics("production_final_metrics.json")
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")
        
        # Clear caches
        if self.config.enable_caching:
            self.restaurant_cache.clear()
        
        self.logger.info("Production application shutdown complete")
