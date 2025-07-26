#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from helpers.dataHelper import getItems

def test_data_encoding():
    """Test if the JSON data is now loaded with correct UTF-8 encoding"""
    
    items = getItems()
    
    print("Testing JSON data encoding:")
    for item in items:
        print(f"Item ID: {item.id}")
        print(f"  Name: {item.name}")
        print(f"  Attributes: {item.attributes}")
        
        # Check for umlauts in attributes specifically
        for attr in item.attributes:
            attr_str = str(attr)
            if any(char in attr_str for char in ['ä', 'ö', 'ü', 'Ä', 'Ö', 'Ü', 'ß']):
                print(f"  ✓ Found umlaut in attribute: {attr_str}")
            if 'Ã' in attr_str:  # This indicates encoding problem
                print(f"  ✗ Encoding issue detected in: {attr_str}")
        print()

if __name__ == "__main__":
    test_data_encoding()
