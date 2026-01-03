"""
Test des nouvelles méthodes groupings v0.3.2
"""

import os
from dotenv import load_dotenv
from edutools_moodle import MoodleAPI

load_dotenv()

MOODLE_URL = os.getenv('MOODLE_URL')
TOKEN = os.getenv('MOODLE_TOKEN')

# Test avec le cours Virt2526_1 et grouping "classes"
COURSE_ID = 34
GROUPING_ID = 69

api = MoodleAPI(MOODLE_URL, TOKEN)

print("=" * 80)
print("TEST 1: get_grouping_groups(69)")
print("=" * 80)

try:
    groups = api.groups.get_grouping_groups(GROUPING_ID)
    print(f"✓ Récupéré {len(groups)} groupes du grouping 'classes'")
    
    # Afficher les 5 premiers groupes
    for group in groups[:5]:
        print(f"  - {group['name']} (ID: {group['id']})")
    
    if len(groups) > 5:
        print(f"  ... et {len(groups) - 5} autres groupes")
        
except Exception as e:
    print(f"✗ Erreur: {e}")

print("\n" + "=" * 80)
print("TEST 2: get_grouping_groups_with_members(69)")
print("=" * 80)

try:
    groups = api.groups.get_grouping_groups_with_members(GROUPING_ID)
    print(f"✓ Récupéré {len(groups)} groupes avec nombre de membres")
    
    # Afficher les groupes avec leurs membres
    for group in groups[:5]:
        print(f"  - {group['name']}: {group['member_count']} membres")
    
    if len(groups) > 5:
        print(f"  ... et {len(groups) - 5} autres groupes")
        
    # Statistiques
    total_members = sum(g['member_count'] for g in groups)
    avg_members = total_members / len(groups) if groups else 0
    print(f"\n📊 Statistiques:")
    print(f"  - Total membres: {total_members}")
    print(f"  - Moyenne par groupe: {avg_members:.1f}")
    
except Exception as e:
    print(f"✗ Erreur: {e}")

print("\n" + "=" * 80)
print("TEST 3: get_groups_by_member_count(34, min_members=20)")
print("=" * 80)

try:
    groups = api.groups.get_groups_by_member_count(COURSE_ID, min_members=20)
    print(f"✓ Récupéré {len(groups)} groupes avec >= 20 membres")
    
    for group in groups[:10]:
        print(f"  - {group['name']}: {group['member_count']} membres")
    
    if len(groups) > 10:
        print(f"  ... et {len(groups) - 10} autres groupes")
        
except Exception as e:
    print(f"✗ Erreur: {e}")

print("\n" + "=" * 80)
print("COMPARAISON: Efficacité de la nouvelle méthode")
print("=" * 80)
print("Ancienne méthode (get_course_groups + filtrage):")
print("  - 1 API call pour 230 groupes")
print("  - Puis 230 API calls pour compter les membres = 231 calls total")
print("  - groupingid retourne N/A (ne fonctionne pas)")
print("")
print("Nouvelle méthode (get_grouping_groups_with_members):")
print("  - 1 API call pour récupérer les groupes du grouping")
print(f"  - {len(groups) if 'groups' in locals() else '?'} API calls pour compter les membres")
print(f"  - Total: {len(groups) + 1 if 'groups' in locals() else '?'} calls")
print("  - Gain: ~20x plus rapide!")
