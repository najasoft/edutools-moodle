# Plan d'ajout des méthodes Groupings dans edutools-moodle v0.3.2

## Étape 1: Nouvelles fonctions Moodle et permissions requises

### Fonctions Moodle Web Services à ajouter:

1. **`core_group_get_grouping_groups`** - NON DISPONIBLE dans version Moodle actuelle
   - Alternative: Utiliser `core_group_get_course_groups` + filtrage côté client

2. **`core_group_assign_grouping`** 
   - Permission: `moodle/course:managegroups`
   - Description: Assigner un groupe à un grouping
   - Paramètres: groupingid, groupid

3. **`core_group_unassign_grouping`**
   - Permission: `moodle/course:managegroups`
   - Description: Retirer un groupe d'un grouping
   - Paramètres: groupingid, groupid

## Étape 2: Nouvelles méthodes à ajouter dans MoodleGroups

### Méthodes de lecture (déjà existantes ou à améliorer):
- ✅ `get_course_groupings(course_id)` - Existe
- ✅ `get_grouping_by_name(course_id, name)` - Existe
- ✅ `create_or_get_grouping(course_id, name, description)` - Existe

### Nouvelles méthodes à créer:

1. **`get_grouping_groups(grouping_id: int)`**
   - Récupère tous les groupes associés à un grouping
   - Utilise `get_course_groups()` + filtrage par `groupingid`
   - Retourne: List[Dict[str, Any]]

2. **`get_grouping_groups_with_members(grouping_id: int, course_id: int)`**
   - Récupère les groupes d'un grouping AVEC leur nombre de membres
   - Enrichit chaque groupe avec member_count
   - Retourne: List[Dict[str, Any]] avec clé 'member_count'

3. **`assign_group_to_grouping(grouping_id: int, group_id: int)`**
   - Assigne un groupe à un grouping
   - API: core_group_assign_grouping
   - Retourne: bool (succès)

4. **`unassign_group_from_grouping(grouping_id: int, group_id: int)`**
   - Retire un groupe d'un grouping
   - API: core_group_unassign_grouping
   - Retourne: bool (succès)

5. **`get_groups_by_member_count(course_id: int, min_members: int = 1)`**
   - Filtre les groupes par nombre minimum de membres
   - Utile pour identifier les groupes-classes
   - Retourne: List[Dict[str, Any]] avec 'member_count'

## Étape 3: Tests à créer

- `test_get_grouping_groups()` - Test récupération groupes d'un grouping
- `test_get_grouping_groups_with_members()` - Test avec membres
- `test_assign_group_to_grouping()` - Test assignation
- `test_unassign_group_from_grouping()` - Test désassignation
- `test_get_groups_by_member_count()` - Test filtrage par taille

## Étape 4: Documentation à mettre à jour

### PERMISSIONS.md
- Ajouter `core_group_assign_grouping` (moodle/course:managegroups)
- Ajouter `core_group_unassign_grouping` (moodle/course:managegroups)

### README.md
- Ajouter exemples d'utilisation des nouvelles méthodes
- Section "Gestion des groupings avancée"

### CHANGELOG.md
- Version 0.3.2
- Nouvelles méthodes groupings

## Étape 5: Version et publication

- Incrémenter version à 0.3.2 dans:
  - setup.py
  - __init__.py
  - README.md badges
- Commit + tag v0.3.2
- Publish to PyPI

## Étape 6: Mise à jour de MoodleGrader

- Installer edutools-moodle 0.3.2
- Utiliser `get_grouping_groups_with_members(grouping_id, course_id)`
- Tester avec cours Virt2526_1
