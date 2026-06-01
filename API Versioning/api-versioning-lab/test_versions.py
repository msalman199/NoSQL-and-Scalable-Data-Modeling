import requests
import json

BASE_URL = "http://localhost:5000"

def compare_versions():
    """
    Compare responses between API versions.
    """
    # TODO: Fetch user from v1
    # TODO: Fetch same user from v2
    # TODO: Print differences in response structure
    # TODO: Check for deprecation headers in v1
    # TODO: Verify v2 has additional fields
    pass

def test_backward_compatibility():
    """
    Verify v1 endpoints still function correctly.
    """
    # TODO: Test all v1 endpoints
    # TODO: Verify response format matches v1 spec
    # TODO: Confirm no breaking changes
    pass

if __name__ == "__main__":
    print("Testing API Versioning...")
    compare_versions()
    test_backward_compatibility()
