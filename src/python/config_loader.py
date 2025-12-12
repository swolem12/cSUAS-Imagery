#!/usr/bin/env python3
"""
Configuration loader for cSUAS detection system
Loads and validates YAML configuration files
"""

import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Load and manage detection configuration"""
    
    def __init__(self, config_path: str = "config/detection_config.yaml"):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            print(f"Warning: Config file not found at {self.config_path}")
            print("Using default configuration")
            self._set_default_config()
            return
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            print(f"Configuration loaded from {self.config_path}")
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Using default configuration")
            self._set_default_config()
    
    def _set_default_config(self):
        """Set default configuration values"""
        self.config = {
            'model': {
                'path': 'models/best.pt',
                'type': 'yolov8',
                'confidence_threshold': 0.5,
                'nms_threshold': 0.4,
                'input_size': [416, 416]
            },
            'source': {
                'device': 0,
                'resolution': [1920, 1080],
                'fps': 30
            },
            'detection': {
                'classes': ['drone'],
                'min_size': 20,
                'max_size': 1000
            },
            'output': {
                'save_video': False,
                'video_path': 'output/detections.mp4',
                'display': True,
                'save_logs': True,
                'log_path': 'output/detections.log'
            },
            'raspberry_pi': {
                'optimize': True,
                'threads': 4,
                'use_gpu': False
            },
            'alerts': {
                'enabled': True,
                'threshold': 3,
                'sound': True,
                'message': 'Drone detected!'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'model.path')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: str = None):
        """
        Save configuration to YAML file
        
        Args:
            path: Output path (uses original path if not specified)
        """
        output_path = Path(path) if path else self.config_path
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            print(f"Configuration saved to {output_path}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration section"""
        return self.get('model', {})
    
    def get_source_config(self) -> Dict[str, Any]:
        """Get source configuration section"""
        return self.get('source', {})
    
    def get_detection_config(self) -> Dict[str, Any]:
        """Get detection configuration section"""
        return self.get('detection', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration section"""
        return self.get('output', {})
    
    def __repr__(self) -> str:
        """String representation"""
        return f"ConfigLoader(config_path='{self.config_path}')"


if __name__ == '__main__':
    # Test configuration loader
    config = ConfigLoader()
    print("\nModel config:", config.get_model_config())
    print("\nSource config:", config.get_source_config())
    print("\nDetection config:", config.get_detection_config())
