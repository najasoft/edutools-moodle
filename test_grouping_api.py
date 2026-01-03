"""
Test des API Moodle pour groupings
"""
import os
from dotenv import load_dotenv
from edutools_moodle import MoodleAPI

load_dotenv()

MOODLE_URL = os.getenv('MOODLE_URL')
TOKEN = os.getenv('MOODLE_TOKEN')

moodle = MoodleAPI(MOODLE_URL, TOKEN)

print("\n" + "="*80)
print("Test des fonctions Moodle pour groupings")
print("="*80)

# Test 1: core_group_assign_grouping
print("\nTest 1: core_group_assign_grouping")
functions = []
try:
    # Ne pas vraiment exécuter, juste tester si la fonction existe
    # On peut vérifier avec check_permissions
    result = moodle.check_permissions(verbose=False)
    
    if isinstance(result, dict):
        functions = [f[0] for f in result.get('granted', [])] + [f[0] for f in result.get('denied', [])]
    
    if 'core_group_assign_grouping' in functions:
        print("✓ core_group_assign_grouping est disponible")
    else:
        print("✗ core_group_assign_grouping n'est PAS disponible")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 2: core_group_unassign_grouping  
print("\nTest 2: core_group_unassign_grouping")
try:
    if 'core_group_unassign_grouping' in functions:
        print("✓ core_group_unassign_grouping est disponible")
    else:
        print("✗ core_group_unassign_grouping n'est PAS disponible")
except Exception as e:
    print(f"✗ Erreur: {e}")

# Test 3: Lister toutes les fonctions group/grouping disponibles
print("\nTest 3: Fonctions group/grouping disponibles:")
try:
    group_functions = [f for f in functions if 'group' in f.lower()]
    for func in sorted(group_functions):
        print(f"  - {func}")
except Exception as e:
    print(f"✗ Erreur: {e}")

print("\n" + "="*80)
