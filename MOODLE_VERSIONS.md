# Compatibilité des Versions Moodle

## Version Minimale Recommandée

**Moodle 3.9 ou supérieur**

Le package `edutools-moodle` utilise des fonctions de l'API Web Services de Moodle qui sont stables depuis la version 3.9 (sortie en mai 2020).

## Fonctions API Utilisées et Versions Minimales

### Core Functions (Disponibles depuis Moodle 2.2+)
- `core_webservice_get_site_info` - Moodle 2.2+ ✅
  - Utilisée par: `MoodleAPI.get_site_info()`

### Groups Functions (Disponibles depuis Moodle 2.3+)
- `core_group_get_groups` - Moodle 2.3+ ✅
  - Utilisée par: `get_course_groups()`
- `core_group_create_groups` - Moodle 2.3+ ✅
  - Utilisée par: `create_group()`
- `core_group_delete_groups` - Moodle 2.3+ ✅
  - Utilisée par: `delete_group()`
- `core_group_add_group_members` - Moodle 2.3+ ✅
  - Utilisée par: `add_user_to_group()`, `batch_enroll_users_to_groups()`
- `core_group_delete_group_members` - Moodle 2.3+ ✅
  - Utilisée par: `remove_member_from_group()`
- `core_group_get_group_members` - Moodle 2.3+ ✅
  - Utilisée par: `get_group_members()`, `get_group_members_info()`
- `core_group_get_course_user_groups` - Moodle 2.9+ ✅
  - Utilisée par: `get_user_groups()`, `get_user_groups_with_names()`

### Cohorts Functions (Disponibles depuis Moodle 2.5+)
- `core_cohort_get_cohort_members` - Moodle 2.5+ ✅
  - Utilisée par: `is_user_in_cohort()`
- `core_cohort_add_cohort_members` - Moodle 2.5+ ✅
  - Utilisée par: `enroll_user_in_cohort()`

### Groupings Functions (Disponibles depuis Moodle 2.3+)
- `core_group_create_groupings` - Moodle 2.3+ ✅
  - Utilisée par: `create_or_get_grouping()`
- `core_group_get_course_groupings` - Moodle 2.3+ ✅
  - Utilisée par: `create_or_get_grouping()`

### Users Functions (Disponibles depuis Moodle 2.2+)
- `core_user_get_users_by_field` - Moodle 2.5+ ✅
  - Utilisée par: `get_users_by_field()`, `check_username_exists()`, `get_student_name()`
- `core_user_create_users` - Moodle 2.2+ ✅
  - Utilisée par: `create_user()`
- `core_message_send_instant_messages` - Moodle 2.9+ ✅
  - Utilisée par: `send_notification()`

### Enrollment Functions (Disponibles depuis Moodle 2.2+)
- `enrol_manual_enrol_users` - Moodle 2.2+ ✅
  - Utilisée par: `enroll_user_in_course()`
- `core_enrol_get_enrolled_users` - Moodle 2.2+ ✅
  - Utilisée par: `is_user_enrolled()`

### Grades Functions (Disponibles depuis Moodle 2.2+)
- `core_grades_update_grades` - Moodle 3.2+ ✅
  - Utilisée par: `add_grade()`, `add_grades()`, `update_grade()`
- `gradereport_user_get_grade_items` - Moodle 2.9+ ✅
  - Utilisée par: `get_grades()`, `get_grade_items()`, `get_grades_for_assignment()`
- `gradereport_user_get_grades_table` - Moodle 3.2+ ✅
  - Utilisée par: `get_course_grades()`

### Assignments Functions (Disponibles depuis Moodle 2.4+)
- `mod_assign_get_assignments` - Moodle 2.4+ ✅
  - Utilisée par: `get_assignments()`, `get_assignment_id_by_cmid()`
- `mod_assign_get_submissions` - Moodle 2.4+ ✅
  - Utilisée par: `get_submissions()`, `get_assignment_submissions()`, `get_user_submission()`

## Tableau de Compatibilité

| Version Moodle | Compatibilité | Fonctionnalités |
|----------------|---------------|-----------------|
| 2.2 - 2.4      | ❌ Non testée | Fonctions de base seulement |
| 2.5 - 2.8      | ⚠️ Partielle  | Certaines fonctions manquantes |
| 2.9 - 3.1      | ⚠️ Partielle  | La plupart des fonctions disponibles |
| **3.2 - 3.8**  | ✅ Compatible | Toutes les fonctions disponibles |
| **3.9 - 4.0**  | ✅ **Recommandée** | Stable et testé |
| **4.1+**       | ✅ Compatible | Dernières versions |

## Fonctions Nécessitant Moodle 3.2+

Les fonctions suivantes nécessitent **au minimum Moodle 3.2** :

1. **Grades Module**
   - `add_grade()` - Nécessite `core_grades_update_grades`
   - `add_grades()` - Nécessite `core_grades_update_grades`
   - `update_grade()` - Nécessite `core_grades_update_grades`
   - `get_course_grades()` - Nécessite `gradereport_user_get_grades_table`

Si vous utilisez une version de Moodle **< 3.2**, ces fonctions ne fonctionneront pas.

## Vérification de la Version

Le package fournit une méthode pour vérifier la version de Moodle :

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://votre-moodle.com", "token")

# Récupérer les informations du site
info = moodle.get_site_info()
print(f"Moodle version: {info['release']}")
print(f"Site name: {info['sitename']}")

# Vérifier la compatibilité
if moodle.check_moodle_version("3.9"):
    print("✅ Version Moodle compatible")
else:
    print("❌ Version Moodle trop ancienne, 3.9+ requis")
```

## Recommandations

### Version de Production
- **Moodle 3.9 LTS** (Support jusqu'en novembre 2023)
- **Moodle 4.1 LTS** (Support jusqu'en décembre 2025)

### Pour Nouveaux Projets
- **Moodle 4.3+** (dernière version stable)

### Activation des Web Services

Pour utiliser ce package, les Web Services doivent être activés dans Moodle :

1. **Administration du site** > **Serveur** > **Services web**
2. Cocher **"Activer les services web"**
3. Cocher **"Activer les protocoles"** > **REST**
4. Créer un service et ajouter les fonctions nécessaires (voir liste ci-dessus)
5. Générer un token pour votre utilisateur

## Fonctions Futures (Roadmap)

Certaines fonctions pourraient nécessiter des versions plus récentes :

- **Quiz API** (Moodle 3.1+)
- **Calendar API** (Moodle 3.3+)
- **Badges API** (Moodle 3.6+)
- **Custom Fields API** (Moodle 3.7+)

## Support

Si vous rencontrez des problèmes de compatibilité :

1. Vérifiez votre version Moodle : `moodle.get_site_info()`
2. Consultez la documentation Moodle officielle : https://docs.moodle.org/dev/Web_services
3. Ouvrez une issue sur GitHub avec les détails de votre configuration

---

**Dernière mise à jour :** 21 décembre 2024  
**Package version :** 0.1.0
