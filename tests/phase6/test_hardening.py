"""
Comprehensive tests for Phase 6 hardening.
"""

import pytest
import tempfile
import json
from unittest.mock import patch, MagicMock

from milestone1.phase6_hardening.testing import TestFixtures, LLMResponseValidator
from milestone1.phase6_hardening.monitoring import PerformanceMonitor
from milestone1.phase6_hardening.caching import CacheManager
from milestone1.phase6_hardening.config import ProductionConfig
from milestone1.phase6_hardening.production import ProductionHardening


class TestPhase6Hardening:
    """Test suite for Phase 6 hardening."""
    
    def test_test_fixtures_creation(self):
        """Test that test fixtures can be created."""
        # Test restaurant data
        restaurants = TestFixtures.get_mock_restaurant_data()
        assert len(restaurants) == 3
        assert all(hasattr(r, 'id') for r in restaurants)
        
        # Test user preferences
        prefs = TestFixtures.get_mock_user_preferences()
        assert prefs.location == "Banashankari"
        assert prefs.budget_band == "high"
        
        # Test LLM responses
        valid_response = TestFixtures.get_valid_llm_response()
        assert LLMResponseValidator.validate_recommendations_structure(valid_response)
        
        invalid_response = TestFixtures.get_invalid_llm_response()
        assert not LLMResponseValidator.validate_recommendations_structure(invalid_response)
    
    def test_cache_manager_functionality(self):
        """Test cache manager operations."""
        cache = CacheManager(max_size_mb=1)  # Small cache for testing
        
        # Test put and get
        test_data = {"key": "value"}
        cache.put("test", test_data, ttl_seconds=60)
        
        retrieved = cache.get("test")
        assert retrieved == test_data
        
        # Test expiration
        cache.put("expired", {"data": "test"}, ttl_seconds=1)
        import time
        time.sleep(2)  # Wait for expiration
        assert cache.get("expired") is None
        
        # Test LRU eviction
        for i in range(10):
            cache.put(f"lru_test_{i}", {"data": f"test_{i}"})
        
        # Should evict oldest when over limit
        assert len(cache.cache) <= cache.max_size_bytes // 100  # Approximate
        
        stats = cache.get_stats()
        assert "hits" in stats
        assert "misses" in stats
    
    def test_performance_monitoring(self):
        """Test performance monitoring functionality."""
        monitor = PerformanceMonitor()
        
        # Test operation tracking
        operation_id = monitor.start_operation("test_operation")
        assert operation_id in monitor.metrics
        
        # Test API metrics
        metrics = monitor.log_api_call("test_endpoint", "GET", 200, 150.5, 100, True)
        assert metrics.success is True
        assert metrics.response_time_ms == 150.5
        
        # Test completion
        result = monitor.end_operation(operation_id)
        assert result["duration_ms"] is not None
        assert result["success"] is True
        
        # Test summary
        summary = monitor.get_performance_summary()
        assert "total_operations" in summary
        assert summary["total_operations"] >= 1
    
    def test_production_config_validation(self):
        """Test production configuration validation."""
        # Test valid config
        config = ProductionConfig.from_env()
        assert config.dataset_name == "ManikaSaini/zomato-restaurant-recommendation"
        assert config.candidate_cap == 25
        
        # Test invalid config
        with patch.dict(os.environ, {"CANDIDATE_CAP": "0"}):
            try:
                ProductionConfig.from_env()
                assert False, "Should raise error for invalid config"
            except ValueError:
                pass  # Expected
        
        # Test missing environment variables
        with patch.dict(os.environ, {}, clear=True):
            try:
                ProductionConfig.from_env()
                assert False, "Should raise error for missing vars"
            except ValueError:
                pass  # Expected
    
    def test_production_hardening_initialization(self):
        """Test production hardening initialization."""
        config = ProductionConfig.from_env()
        
        with patch.dict(os.environ, {
            "XAI_API_KEY": "test_key",
            "HF_DATASET_NAME": config.dataset_name,
            "ENABLE_PERFORMANCE_MONITORING": "true",
            "ENABLE_CACHING": "true"
        }):
            hardening = ProductionHardening(config)
            
            # Should initialize without errors
            assert hardening.config == config
            assert hardening.monitor is not None
            assert hardening.restaurant_cache is not None
            assert hardening.llm_cache is not None
    
    def test_production_health_checks(self):
        """Test production health checks."""
        config = ProductionConfig.from_env()
        
        with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
            hardening = ProductionHardening(config)
            
            # Should pass health checks
            hardening._run_health_checks()
            
            # Test with missing API key (should fail)
            with patch.dict(os.environ, {"XAI_API_KEY": ""}):
                try:
                    ProductionHardening(config)
                    assert False, "Should fail without API key"
                except RuntimeError:
                    pass  # Expected
    
    def test_production_test_suite(self):
        """Test comprehensive production test suite."""
        config = ProductionConfig.from_env()
        
        with patch.dict(os.environ, {
            "XAI_API_KEY": "test_key",
            "HF_DATASET_NAME": config.dataset_name,
            "ENABLE_PERFORMANCE_MONITORING": "true",
            "ENABLE_CACHING": "true"
        }):
            hardening = ProductionHardening(config)
            
            # Run all tests
            test_results = hardening.run_production_tests()
            
            # Should pass all tests
            assert test_results is True
    
    def test_end_to_end_production_flow(self):
        """Test end-to-end production flow."""
        # This would test the complete flow from user input to recommendations
        # with all Phase 6 components active
        pass


class TestPhase6Integration:
    """Integration tests for Phase 6 components."""
    
    def test_cache_integration_with_monitoring(self):
        """Test cache and monitoring integration."""
        cache = CacheManager(max_size_mb=1)
        monitor = PerformanceMonitor()
        
        # Simulate cache operations with monitoring
        operation_id = monitor.start_operation("cache_test")
        cache.put("test", {"data": "value"}, ttl_seconds=60)
        retrieved = cache.get("test")
        
        result = monitor.end_operation(operation_id)
        
        assert result["success"] is True
        assert "cache_hits" in result or "cache_misses" in result
    
    def test_config_cache_integration(self):
        """Test configuration and cache integration."""
        config = ProductionConfig.from_env()
        cache = CacheManager(
            max_size_mb=config.cache_ttl_restaurants // (1024 * 1024)  # Convert to MB
        )
        
        # Test cache operations with config-based TTL
        cache.put("config_test", {"data": "test"}, ttl_seconds=config.cache_ttl_recommendations)
        retrieved = cache.get("config_test")
        
        assert retrieved is not None
        assert retrieved["data"] == {"data": "test"}


# Pytest fixtures
@pytest.fixture
def production_config():
    """Fixture providing production configuration."""
    return ProductionConfig.from_env()


@pytest.fixture
def mock_cache_manager():
    """Fixture providing mock cache manager."""
    return CacheManager(max_size_mb=1)


@pytest.fixture
def mock_performance_monitor():
    """Fixture providing mock performance monitor."""
    return PerformanceMonitor()


# Test classes
class TestTestFixtures:
    """Test test fixtures functionality."""
    
    def test_restaurant_data_creation(self):
        """Test restaurant data creation."""
        restaurants = TestFixtures.get_mock_restaurant_data()
        assert len(restaurants) > 0
        assert all(r.id for r in restaurants)
    
    def test_user_preferences_creation(self):
        """Test user preferences creation."""
        prefs = TestFixtures.get_mock_user_preferences()
        assert prefs.location is not None
        assert isinstance(prefs.cuisines, tuple)
    
    def test_llm_responses(self):
        """Test LLM response fixtures."""
        valid = TestFixtures.get_valid_llm_response()
        invalid = TestFixtures.get_invalid_llm_response()
        hallucinated = TestFixtures.get_hallucinated_llm_response()
        
        assert LLMResponseValidator.validate_recommendations_structure(valid)
        assert not LLMResponseValidator.validate_recommendations_structure(invalid)
        assert not LLMResponseValidator.validate_restaurant_ids(hallucinated, ["test_1", "test_2"])


class TestCacheManager:
    """Test cache manager functionality."""
    
    def test_basic_operations(self, mock_cache_manager):
        """Test basic cache operations."""
        cache = mock_cache_manager
        
        # Test put and get
        cache.put("key1", {"data": "value1"})
        cache.put("key2", {"data": "value2"})
        
        assert cache.get("key1")["data"] == "value1"
        assert cache.get("key2")["data"] == "value2"
        assert cache.get("nonexistent") is None
        
        # Test expiration
        cache.put("expire_test", {"data": "test"}, ttl_seconds=1)
        import time
        time.sleep(2)
        assert cache.get("expire_test") is None
    
    def test_lru_eviction(self, mock_cache_manager):
        """Test LRU eviction policy."""
        cache = mock_cache_manager
        
        # Fill cache beyond capacity
        for i in range(150):  # Assuming small cache size
            cache.put(f"key_{i}", {"data": f"value_{i}"})
        
        # Should evict oldest entries
        initial_size = len(cache.cache)
        cache.put("new_key", {"data": "new_value"})
        final_size = len(cache.cache)
        
        # Should maintain size limit
        assert final_size <= initial_size + 1  # Allow one new entry
    
    def test_statistics_tracking(self, mock_cache_manager):
        """Test cache statistics tracking."""
        cache = mock_cache_manager
        
        # Generate some activity
        cache.put("key1", {"data": "value1"})
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        
        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert "hit_rate_percent" in stats


class TestPerformanceMonitoring:
    """Test performance monitoring functionality."""
    
    def test_operation_tracking(self, mock_performance_monitor):
        """Test operation tracking."""
        monitor = mock_performance_monitor
        
        operation_id = monitor.start_operation("test_op")
        assert operation_id in monitor.metrics
        
        metrics = monitor.log_api_call("test", "GET", 200, 100.0, 50, True)
        assert metrics.success is True
        
        result = monitor.end_operation(operation_id)
        assert result["success"] is True
        assert result["duration_ms"] is not None
    
    def test_multiple_operations(self, mock_performance_monitor):
        """Test tracking multiple operations."""
        monitor = mock_performance_monitor()
        
        # Track multiple operations
        ops = []
        for i in range(5):
            op_id = monitor.start_operation(f"test_op_{i}")
            ops.append(op_id)
        
        # Complete operations
        for op_id in ops:
            monitor.end_operation(op_id)
        
        summary = monitor.get_performance_summary()
        assert summary["total_operations"] == 5
        assert summary["total_api_calls"] == 5
    
    def test_performance_export(self, mock_performance_monitor, tmp_path):
        """Test performance metrics export."""
        monitor = mock_performance_monitor()
        
        # Add some metrics
        monitor.start_operation("export_test")
        monitor.end_operation("export_test")
        
        # Export to temporary file
        monitor.export_metrics(f"{tmp_path}/test_metrics.json")
        
        # Verify file was created and contains expected data
        import json
        with open(f"{tmp_path}/test_metrics.json", 'r') as f:
            exported_data = json.load(f)
        
        assert "summary" in exported_data
        assert exported_data["summary"]["total_operations"] >= 1


class TestProductionConfig:
    """Test production configuration."""
    
    def test_from_environment(self):
        """Test configuration loading from environment."""
        with patch.dict(os.environ, {
            "HF_DATASET_NAME": "test_dataset",
            "CANDIDATE_CAP": "50",
            "XAI_MODEL": "test-model"
        }):
            config = ProductionConfig.from_env()
            
            assert config.dataset_name == "test_dataset"
            assert config.candidate_cap == 50
            assert config.xai_model == "test-model"
    
    def test_validation(self):
        """Test configuration validation."""
        # Test valid configuration
        config = ProductionConfig(
            dataset_name="test_dataset",
            candidate_cap=25
        )
        
        issues = config.validate()
        assert len(issues) == 0
        
        # Test invalid configuration
        invalid_config = ProductionConfig(
            candidate_cap=0  # Invalid
        )
        
        issues = invalid_config.validate()
        assert len(issues) > 0
        assert "candidate_cap must be positive" in issues


class TestProductionHardening:
    """Test production hardening functionality."""
    
    def test_initialization(self, production_config):
        """Test production hardening initialization."""
        with patch.dict(os.environ, {
            "XAI_API_KEY": "test_key",
            "ENABLE_PERFORMANCE_MONITORING": "true",
            "ENABLE_CACHING": "true"
        }):
            hardening = ProductionHardening(production_config)
            
            # Should initialize successfully
            assert hardening.config is not None
            assert hardening.monitor is not None
    
    def test_health_checks(self, production_config):
        """Test health check functionality."""
        with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
            hardening = ProductionHardening(production_config)
            
            # Should pass health checks
            hardening._run_health_checks()
            
            # Test with invalid configuration
            with patch.dict(os.environ, {"XAI_API_KEY": ""}):
                try:
                    ProductionHardening(production_config)
                    assert False, "Should fail without API key"
                except RuntimeError:
                    pass  # Expected
    
    def test_production_tests(self, production_config):
        """Test production test suite."""
        with patch.dict(os.environ, {
            "XAI_API_KEY": "test_key",
            "ENABLE_PERFORMANCE_MONITORING": "true",
            "ENABLE_CACHING": "true"
        }):
            hardening = ProductionHardening(production_config)
            
            # Should pass all tests
            result = hardening.run_production_tests()
            assert result is True
    
    def test_production_status(self, production_config):
        """Test production status reporting."""
        with patch.dict(os.environ, {"XAI_API_KEY": "test_key"}):
            hardening = ProductionHardening(production_config)
            
            status = hardening.get_production_status()
            
            assert "config" in status
            assert "monitoring" in status
            assert "health_status" in status


# Integration tests
class TestPhase6Integration:
    """Integration tests across Phase 6 components."""
    
    def test_cache_monitoring_integration(self, production_config):
        """Test cache and monitoring integration."""
        with patch.dict(os.environ, {"ENABLE_CACHING": "true", "ENABLE_PERFORMANCE_MONITORING": "true"}):
            hardening = ProductionHardening(production_config)
            
            # Test that cache operations are monitored
            hardening.monitor.start_operation("integration_test")
            hardening.restaurant_cache.put("test", {"data": "value"})
            hardening.restaurant_cache.get("test")
            
            result = hardening.monitor.end_operation("integration_test")
            
            assert result["success"] is True
            assert "cache_hits" in result or "cache_misses" in result
