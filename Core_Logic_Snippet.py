"""
WhatIF Factory - Core Pipeline Control & Exception Handling Logic

This file demonstrates the architectural patterns used in WhatIF Factory:
- Exponential backoff retry mechanisms
- Comprehensive error classification
- Stateful pipeline recovery
- Cost-aware execution control

These patterns enable production-grade reliability and operational sustainability.
"""

import time
import functools
from typing import Callable, Type, Tuple, Optional, Dict, Any
from pathlib import Path


# ============================================================================
# RETRY MECHANISM WITH EXPONENTIAL BACKOFF
# ============================================================================

def retry_on_failure(
    max_attempts: int = 3,
    delay: float = 2.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for automatic retry with exponential backoff.
    
    This is a core architectural pattern that prevents transient API failures
    from causing full pipeline restarts, reducing wasted API costs.
    
    Args:
        max_attempts: Maximum retry attempts (default: 3)
        delay: Initial delay before first retry in seconds (default: 2.0)
        backoff: Multiplier for delay increase per retry (default: 2.0)
        exceptions: Tuple of exception types to retry on
    
    Example:
        @retry_on_failure(max_attempts=3, delay=2, backoff=2)
        def generate_image(prompt):
            return flux_api.generate(prompt)
        
        # Retry sequence: 2s → 4s → 8s → fail
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                
                except exceptions as e:
                    last_exception = e
                    
                    if attempt >= max_attempts:
                        # Final attempt failed - raise exception
                        raise
                    
                    # Log retry attempt
                    print(f"❌ {func.__name__} failed (attempt {attempt}/{max_attempts})")
                    print(f"   Error: {type(e).__name__}: {str(e)}")
                    print(f"⏳ Retrying in {current_delay:.1f}s...")
                    
                    time.sleep(current_delay)
                    current_delay *= backoff  # Exponential backoff
            
            # Safety net (should not reach here)
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def retry_with_callback(
    max_attempts: int = 3,
    delay: float = 2.0,
    backoff: float = 2.0,
    on_retry: Optional[Callable] = None,
    on_failure: Optional[Callable] = None
):
    """
    Retry decorator with callback functions for custom handling.
    
    Enables integration with logging systems, cost monitoring, and user notifications.
    
    Args:
        max_attempts: Maximum retry attempts
        delay: Initial delay before retry
        backoff: Delay multiplier per retry
        on_retry: Callback function(attempt, exception) called on each retry
        on_failure: Callback function(exception) called on final failure
    
    Example:
        @retry_with_callback(
            max_attempts=3,
            on_retry=lambda attempt, e: logger.warning(f"Retry {attempt}: {e}"),
            on_failure=lambda e: send_alert(f"Critical failure: {e}")
        )
        def critical_api_call():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    
                    if attempt >= max_attempts:
                        # Final failure
                        if on_failure:
                            on_failure(e)
                        raise
                    
                    # Retry callback
                    if on_retry:
                        on_retry(attempt, e)
                    
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


# Pre-configured decorators for common scenarios
def retry_api_call(max_attempts: int = 3):
    """API call retry decorator (network errors only)"""
    import requests
    return retry_on_failure(
        max_attempts=max_attempts,
        delay=2.0,
        backoff=2.0,
        exceptions=(
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        )
    )


def retry_file_operation(max_attempts: int = 3):
    """File operation retry decorator (IO errors only)"""
    return retry_on_failure(
        max_attempts=max_attempts,
        delay=1.0,
        backoff=1.5,
        exceptions=(IOError, OSError)
    )


# ============================================================================
# ERROR CLASSIFICATION SYSTEM
# ============================================================================

class ErrorHandler:
    """
    Comprehensive error classification and user-friendly message generation.
    
    This system classifies errors into 11 categories, enabling:
    - Intelligent recovery strategies
    - User-friendly error messages
    - Detailed logging for debugging
    - Cost tracking (credit-related errors)
    
    Architecture Decision: Separate technical details from user-facing messages
    to improve debugging while maintaining usability.
    """
    
    ERROR_MESSAGES = {
        # API Errors
        'api_unauthorized': {
            'title': '🔑 API Authentication Error',
            'message': 'API key is invalid or expired.',
            'solutions': [
                'Verify API key in .env file',
                'Request new key if expired',
                'Restart application after updating'
            ]
        },
        'api_rate_limit': {
            'title': '⏳ API Rate Limit Exceeded',
            'message': 'API call limit exceeded.',
            'solutions': [
                'Wait before retrying',
                'Free plans have call limits',
                'Consider upgrading to paid plan'
            ]
        },
        'api_insufficient_credits': {
            'title': '💰 Insufficient Credits',
            'message': 'Insufficient credits to complete operation.',
            'solutions': [
                'Recharge credits',
                'Use free resources (Gemini, Veo, Adam voice)',
                'Reduce project settings (fewer scenes)'
            ]
        },
        'api_timeout': {
            'title': '⏱️ API Timeout',
            'message': 'API server did not respond.',
            'solutions': [
                'Check network connection',
                'Retry after waiting',
                'Verify API server status'
            ]
        },
        
        # File Errors
        'file_not_found': {
            'title': '📁 File Not Found',
            'message': 'Required file does not exist.',
            'solutions': [
                'Verify file path',
                'Complete previous pipeline step',
                'Check if file was deleted'
            ]
        },
        'file_permission': {
            'title': '🔒 File Permission Error',
            'message': 'No permission to access file.',
            'solutions': [
                'Run with administrator privileges',
                'Check if file is in use by another program',
                'Verify file permissions'
            ]
        },
        
        # Project Errors
        'project_invalid': {
            'title': '📋 Invalid Project Data',
            'message': 'Project file is corrupted or invalid format.',
            'solutions': [
                'Restore from backup',
                'Recreate project',
                'Verify JSON format'
            ]
        },
        'project_not_found': {
            'title': '📋 Project Not Found',
            'message': 'Specified project does not exist.',
            'solutions': [
                'Verify project ID',
                'Check projects_v2 folder',
                'Create new project'
            ]
        },
        
        # Default
        'unknown': {
            'title': '❌ Unknown Error',
            'message': 'Unexpected error occurred.',
            'solutions': [
                'Check log files (logs/)',
                'Restart application',
                'Contact developer if issue persists'
            ]
        }
    }
    
    @classmethod
    def classify_error(cls, exception: Exception) -> str:
        """
        Classify exception into one of 11 error categories.
        
        This enables intelligent recovery strategies and cost tracking.
        """
        error_str = str(exception).lower()
        error_type = type(exception).__name__
        
        # API errors
        if 'unauthorized' in error_str or '401' in error_str:
            return 'api_unauthorized'
        elif 'rate limit' in error_str or '429' in error_str:
            return 'api_rate_limit'
        elif 'insufficient' in error_str or 'credits' in error_str:
            return 'api_insufficient_credits'
        elif 'timeout' in error_str or error_type == 'Timeout':
            return 'api_timeout'
        
        # File errors
        elif error_type == 'FileNotFoundError' or 'not found' in error_str:
            return 'file_not_found'
        elif error_type == 'PermissionError':
            return 'file_permission'
        
        # Project errors
        elif 'project' in error_str and 'invalid' in error_str:
            return 'project_invalid'
        elif 'project' in error_str and 'not found' in error_str:
            return 'project_not_found'
        
        # Default
        else:
            return 'unknown'
    
    @classmethod
    def get_error_message(cls, exception: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive error information.
        
        Returns:
            Dictionary with:
            - category: Error classification
            - title: User-friendly title
            - message: User-friendly message
            - solutions: List of recovery steps
            - technical_details: Technical information for debugging
        """
        error_category = cls.classify_error(exception)
        template = cls.ERROR_MESSAGES.get(error_category, cls.ERROR_MESSAGES['unknown'])
        
        return {
            'category': error_category,
            'title': template['title'],
            'message': template['message'],
            'solutions': template['solutions'],
            'technical_details': {
                'exception_type': type(exception).__name__,
                'exception_message': str(exception),
                'context': context or {}
            }
        }
    
    @classmethod
    def format_error_for_ui(cls, exception: Exception, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Format error for user interface display.
        
        Architecture Decision: Separate user-facing messages from technical details
        to improve usability while maintaining debugging capability.
        """
        error_info = cls.get_error_message(exception, context)
        
        message = f"{error_info['title']}\n\n"
        message += f"❌ {error_info['message']}\n\n"
        message += "💡 Solutions:\n"
        for i, solution in enumerate(error_info['solutions'], 1):
            message += f"   {i}. {solution}\n"
        
        message += f"\n🔧 Technical: {error_info['technical_details']['exception_type']}"
        
        return message


# ============================================================================
# PIPELINE CONTROL EXAMPLE
# ============================================================================

class PipelineStage:
    """
    Example pipeline stage with integrated error handling.
    
    This demonstrates how retry mechanisms and error classification
    work together in the actual pipeline.
    """
    
    def __init__(self, stage_name: str, cost_per_attempt: float = 0.0):
        self.stage_name = stage_name
        self.cost_per_attempt = cost_per_attempt
        self.total_cost = 0.0
    
    @retry_on_failure(max_attempts=3, delay=2, backoff=2)
    def execute_with_retry(self, operation: Callable, *args, **kwargs):
        """
        Execute operation with automatic retry.
        
        Architecture Pattern: Retry decorator prevents transient failures
        from causing full pipeline restart, saving costs.
        """
        try:
            result = operation(*args, **kwargs)
            return result
        except Exception as e:
            # Classify error for intelligent handling
            error_info = ErrorHandler.get_error_message(e)
            
            # Track cost if credit-related error
            if error_info['category'] == 'api_insufficient_credits':
                self.total_cost += self.cost_per_attempt
            
            # Re-raise for retry mechanism
            raise
    
    def execute_with_callback(self, operation: Callable, *args, **kwargs):
        """
        Execute with callback for logging and monitoring.
        """
        def on_retry(attempt, exception):
            error_info = ErrorHandler.get_error_message(exception)
            print(f"[{self.stage_name}] Retry {attempt}: {error_info['title']}")
        
        def on_failure(exception):
            error_info = ErrorHandler.get_error_message(exception)
            print(f"[{self.stage_name}] Final failure: {error_info['title']}")
            # Could send alert, update status, etc.
        
        @retry_with_callback(
            max_attempts=3,
            on_retry=on_retry,
            on_failure=on_failure
        )
        def _execute():
            return operation(*args, **kwargs)
        
        return _execute()


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("WhatIF Factory - Core Logic Examples")
    print("=" * 80)
    
    # Example 1: Basic retry
    print("\n1. Basic Retry Mechanism:")
    print("-" * 80)
    
    @retry_on_failure(max_attempts=3, delay=1, backoff=2)
    def flaky_api_call():
        """Simulated API call that may fail"""
        import random
        if random.random() < 0.7:  # 70% failure rate
            raise ConnectionError("API timeout")
        return "Success!"
    
    try:
        result = flaky_api_call()
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Failed after retries: {e}")
    
    # Example 2: Error classification
    print("\n2. Error Classification:")
    print("-" * 80)
    
    test_errors = [
        Exception("401 Unauthorized: Invalid API key"),
        Exception("Rate limit exceeded: 429"),
        Exception("Insufficient credits to complete operation"),
        FileNotFoundError("assets/audio/test.mp3 not found")
    ]
    
    for error in test_errors:
        error_info = ErrorHandler.get_error_message(error)
        print(f"\nError: {error}")
        print(f"Category: {error_info['category']}")
        print(f"Title: {error_info['title']}")
        print(f"Solutions: {error_info['solutions'][0]}")
    
    # Example 3: Pipeline stage with error handling
    print("\n3. Pipeline Stage Example:")
    print("-" * 80)
    
    stage = PipelineStage("Image Generation", cost_per_attempt=0.055)
    
    def generate_image(prompt: str):
        """Simulated image generation"""
        import random
        if random.random() < 0.5:
            raise Exception("Insufficient credits to complete operation")
        return f"image_{prompt[:10]}.png"
    
    try:
        result = stage.execute_with_retry(generate_image, "cinematic sunset")
        print(f"✅ Generated: {result}")
    except Exception as e:
        error_msg = ErrorHandler.format_error_for_ui(e)
        print(f"❌ Failed:\n{error_msg}")
        print(f"💰 Total cost: ${stage.total_cost:.3f}")
    
    print("\n" + "=" * 80)
    print("✅ Examples completed")
    print("=" * 80)
