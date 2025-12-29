# Guide d'Exécution des Tests pour MoodleGroups

## 📋 Prérequis

1. **Créer le fichier .env** dans le dossier `tests/` :
   ```bash
   MOODLE_URL=https://votre-moodle.com
   MOODLE_TOKEN=votre_token
   COURSE_ID=123
   GROUP_ID=1811
   USER_ID=776
   GROUPING_ID=64
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Types de Tests

### Tests en Lecture Seule (Safe - Read Only)
Ces tests ne modifient PAS votre instance Moodle. Ils lisent seulement les données.

**Classe : `TestMoodleGroupsBasic`**

1. ✅ `test_get_course_groups` - Liste tous les groupes du cours
2. ✅ `test_get_group_members` - Liste les IDs des membres d'un groupe
3. ✅ `test_get_group_members_info` - Infos détaillées des membres
4. ✅ `test_is_user_in_group` - Vérifie si user est dans un groupe
5. ✅ `test_get_user_groups` - Liste tous les groupes d'un user
6. ✅ `test_get_user_groups_with_names` - Noms des groupes d'un user
7. ✅ `test_get_all_course_groups_dict` - Dict {nom: id} des groupes
8. ✅ `test_get_group_by_name` - Trouve un groupe par nom
9. ✅ `test_get_group_id_by_name` - Trouve l'ID d'un groupe par nom

### Tests en Écriture (⚠️ MODIFIENT Moodle)
Ces tests créent, modifient et suppriment des données dans Moodle.

**Classe : `TestMoodleGroupsWriteOperations`**

10. ⚠️ `test_create_group` - Crée un nouveau groupe
11. ⚠️ `test_create_or_get_group_existing` - Récupère un groupe existant
12. ⚠️ `test_create_or_get_group_new` - Crée un groupe si n'existe pas
13. ⚠️ `test_add_user_to_group` - Ajoute un user à un groupe
14. ⚠️ `test_remove_member_from_group` - Retire un user d'un groupe
15. ⚠️ `test_move_user_to_group` - Déplace un user entre groupes
16. ⚠️ `test_batch_enroll_users_to_groups` - Inscription batch
17. ⚠️ `test_delete_group` - Supprime les groupes de test (cleanup)

**Classe : `TestMoodleGroupingsOperations`**

18. ⚠️ `test_create_or_get_grouping` - Crée/récupère un groupement

**Classe : `TestMoodleCohortsOperations`**

19. ✅ `test_is_user_in_cohort_default` - Vérifie si user dans cohorte
20. ✅ `test_is_user_in_cohort_custom` - Vérifie avec nom personnalisé

## 🚀 Commandes d'Exécution

### Exécuter TOUS les tests
```bash
pytest tests/test_groups.py -v
```

### Exécuter SEULEMENT les tests en lecture seule (SAFE)
```bash
pytest tests/test_groups.py::TestMoodleGroupsBasic -v
```

### Exécuter SEULEMENT les tests d'écriture (ATTENTION)
```bash
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations -v
```

### Exécuter UN SEUL test spécifique
```bash
# Exemple : test get_course_groups
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_course_groups -v

# Exemple : test get_group_members
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_group_members -v

# Exemple : test is_user_in_group
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_is_user_in_group -v
```

### Exécuter avec plus de détails
```bash
pytest tests/test_groups.py -v -s
```
L'option `-s` affiche les prints dans la console.

### Exécuter et arrêter au premier échec
```bash
pytest tests/test_groups.py -v -x
```

## 📝 Ordre d'Exécution Recommandé

### Phase 1 : Validation des Tests en Lecture Seule
Commencez par valider que les lectures fonctionnent :

```bash
# Test 1 : Liste des groupes
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_course_groups -v -s

# Test 2 : Membres d'un groupe
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_group_members -v -s

# Test 3 : Infos détaillées des membres
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_group_members_info -v -s

# Test 4 : Vérifier si user dans groupe
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_is_user_in_group -v -s

# Test 5 : Groupes d'un user
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_user_groups -v -s

# Test 6 : Noms des groupes d'un user
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_user_groups_with_names -v -s

# Test 7 : Dict des groupes
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_all_course_groups_dict -v -s

# Test 8 : Trouver groupe par nom
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_group_by_name -v -s

# Test 9 : Trouver ID par nom
pytest tests/test_groups.py::TestMoodleGroupsBasic::test_get_group_id_by_name -v -s
```

### Phase 2 : Tests en Écriture (UN PAR UN avec validation)

⚠️ **ATTENTION** : Ces tests modifient votre instance Moodle !

```bash
# Test 10 : Créer un groupe
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_create_group -v -s
# ➡️ VALIDEZ dans Moodle que le groupe est créé avant de continuer

# Test 11 : Récupérer groupe existant
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_create_or_get_group_existing -v -s

# Test 12 : Créer nouveau groupe si n'existe pas
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_create_or_get_group_new -v -s

# Test 13 : Ajouter user au groupe
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_add_user_to_group -v -s
# ➡️ VALIDEZ dans Moodle que le user est ajouté

# Test 14 : Retirer user du groupe
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_remove_member_from_group -v -s
# ➡️ VALIDEZ dans Moodle que le user est retiré

# Test 15 : Déplacer user entre groupes
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_move_user_to_group -v -s

# Test 16 : Inscription batch
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_batch_enroll_users_to_groups -v -s

# Test 17 : CLEANUP - Supprimer les groupes de test
pytest tests/test_groups.py::TestMoodleGroupsWriteOperations::test_delete_group -v -s
# ➡️ VALIDEZ dans Moodle que les groupes de test sont supprimés
```

### Phase 3 : Tests Groupements et Cohortes

```bash
# Test 18 : Groupements
pytest tests/test_groups.py::TestMoodleGroupingsOperations::test_create_or_get_grouping -v -s

# Test 19-20 : Cohortes
pytest tests/test_groups.py::TestMoodleCohortsOperations -v -s
```

## 📊 Exemple de Sortie Attendue

```
tests/test_groups.py::TestMoodleGroupsBasic::test_get_course_groups 
📋 Testing get_course_groups for course_id=123
✅ Found 5 groups in the course
   First group: Group A (ID: 1)
PASSED

tests/test_groups.py::TestMoodleGroupsBasic::test_get_group_members 
👥 Testing get_group_members for group_id=1811
✅ Found 3 members in the group
   Member IDs: [776, 777, 778]
PASSED
```

## ⚠️ Important

1. **Toujours valider après les tests d'écriture** : Vérifiez dans votre interface Moodle que les modifications ont bien été appliquées.

2. **Les tests créent des groupes temporaires** : Les groupes créés ont des noms comme `TestGroup_20251223_143045`.

3. **Le test `test_delete_group` nettoie** : Il supprime automatiquement les groupes créés pendant les tests.

4. **Permissions requises** : Votre token doit avoir les permissions pour créer/modifier/supprimer des groupes.

## 🔧 Dépannage

### Erreur : "MOODLE_URL and MOODLE_TOKEN must be set"
➡️ Créez le fichier `.env` dans le dossier `tests/`

### Erreur : "No module named 'dotenv'"
➡️ Exécutez : `pip install python-dotenv`

### Erreur : "No module named 'pytest'"
➡️ Exécutez : `pip install pytest`

### Test échoue avec "MoodleAuthenticationError"
➡️ Vérifiez que votre token est valide et que les web services sont activés

### Test échoue avec "404" ou "ResourceNotFound"
➡️ Vérifiez que les IDs (COURSE_ID, GROUP_ID, USER_ID) sont corrects
