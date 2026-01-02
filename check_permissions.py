#!/usr/bin/env python
"""
Script CLI pour vérifier les permissions Moodle Web Services.

Ce script vérifie que toutes les fonctions Moodle requises par edutools-moodle
sont autorisées dans votre configuration Web Services.

Usage:
    python check_permissions.py
    
Prérequis:
    - Fichier .env avec MOODLE_URL et MOODLE_TOKEN
    - Ou variables d'environnement MOODLE_URL et MOODLE_TOKEN
"""

import os
import sys
from pathlib import Path

# Add package to path for development mode
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Main function to check Moodle permissions."""
    print("\n" + "="*80)
    print("EDUTOOLS-MOODLE PERMISSION CHECKER")
    print("="*80)
    
    # Try to load .env file
    try:
        from dotenv import load_dotenv
        if Path('.env').exists():
            load_dotenv()
            print("✅ Loaded configuration from .env file")
        else:
            print("ℹ️  No .env file found, using environment variables")
    except ImportError:
        print("ℹ️  python-dotenv not installed, using environment variables only")
    
    # Get credentials
    moodle_url = os.getenv('MOODLE_URL')
    moodle_token = os.getenv('MOODLE_TOKEN')
    
    if not moodle_url or not moodle_token:
        print("\n❌ ERROR: Missing configuration!")
        print("\nPlease set the following environment variables:")
        print("  MOODLE_URL=https://your-moodle-site.com")
        print("  MOODLE_TOKEN=your_webservice_token")
        print("\nOr create a .env file with these variables.")
        return 1
    
    print(f"🌐 Moodle URL: {moodle_url}")
    print(f"🔑 Token: {moodle_token[:10]}..." if len(moodle_token) > 10 else f"🔑 Token: {moodle_token}")
    
    # Import and initialize API
    try:
        from edutools_moodle import MoodleAPI
        moodle = MoodleAPI(moodle_url, moodle_token)
    except Exception as e:
        print(f"\n❌ ERROR: Failed to initialize Moodle API: {e}")
        return 1
    
    # Get site info
    try:
        info = moodle.get_site_info()
        print(f"\n✅ Connected to: {info.get('sitename', 'Unknown')}")
        print(f"👤 User: {info.get('fullname', info.get('username', 'Unknown'))}")
        print(f"📦 Moodle version: {info.get('release', 'Unknown')}")
    except Exception as e:
        print(f"\n⚠️  Warning: Could not get site info: {e}")
    
    # Check permissions
    try:
        result = moodle.check_permissions(verbose=True)
        
        # Return exit code based on results
        if result['denied'] > 0:
            print("\n" + "="*80)
            print("❌ CONFIGURATION INCOMPLETE")
            print("="*80)
            print(f"\nYou need to add {result['denied']} functions to your Moodle web service.")
            print("\nSteps to fix:")
            print("1. Log in to Moodle as administrator")
            print("2. Go to: Site Administration → Plugins → Web Services → Manage Services")
            print("3. Edit your web service and add the missing functions listed above")
            print("\nFor detailed instructions, see: PERMISSIONS.md")
            return 1
        else:
            print("\n" + "="*80)
            print("✅ CONFIGURATION COMPLETE")
            print("="*80)
            print("\nAll required permissions are properly configured!")
            print("You can now use edutools-moodle without restrictions.")
            return 0
            
    except Exception as e:
        print(f"\n❌ ERROR during permission check: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
