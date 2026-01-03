# Permissions Moodle requises pour edutools-moodle

## Module: MoodleCourses

Les fonctions suivantes nécessitent des permissions spécifiques dans Moodle Web Services :

### Fonctions principales

| Fonction | Permission Moodle requise | Description |
|----------|---------------------------|-------------|
| `get_user_courses()` | `core_enrol_get_users_courses` | Récupérer les cours d'un utilisateur |
| `get_enrolled_users()` | `core_enrol_get_enrolled_users` | Lister les utilisateurs inscrits dans un cours |
| `get_course_by_field()` | `core_course_get_courses_by_field` | Rechercher des cours par champ |
| `get_categories()` | `core_course_get_categories` | Lister les catégories de cours |
| `get_course_contents()` | `core_course_get_contents` | Récupérer le contenu d'un cours |
| `get_recent_courses()` | `core_course_get_recent_courses` | Lister les cours récemment consultés |
| `search_courses()` | `core_course_search_courses` | Rechercher des cours par nom/résumé |

### Permissions additionnelles

- `core_webservice_get_site_info` - Nécessaire pour obtenir l'ID de l'utilisateur authentifié

## Module: MoodleGroups

| Fonction | Permission Moodle requise | Permission utilisateur |
|----------|---------------------------|------------------------|
| `get_course_groups()` | `core_group_get_course_groups` | - |
| `get_group_members()` | `core_group_get_group_members` | - |
| `add_user_to_group()` | `core_group_add_group_members` | `moodle/course:managegroups` |
| `remove_user_from_group()` | `core_group_delete_group_members` | `moodle/course:managegroups` |
| `create_group()` | `core_group_create_groups` | `moodle/course:managegroups` |
| `delete_group()` | `core_group_delete_groups` | `moodle/course:managegroups` |
| `get_course_groupings()` | `core_group_get_course_groupings` | - |
| `get_grouping_by_name()` | `core_group_get_course_groupings` | - |
| `create_or_get_grouping()` | `core_group_create_groupings` | `moodle/course:managegroups` |
| `get_grouping_groups()` | `core_group_get_groupings` | - |
| `get_grouping_groups_with_members()` | `core_group_get_groupings`, `core_group_get_group_members` | - |
| `assign_group_to_grouping()` | `core_group_assign_grouping` | `moodle/course:managegroups` |
| `unassign_group_from_grouping()` | `core_group_unassign_grouping` | `moodle/course:managegroups` |

## Module: MoodleAssignments

| Fonction | Permission Moodle requise |
|----------|---------------------------|
| `get_assignments()` | `mod_assign_get_assignments` |
| `get_submissions()` | `mod_assign_get_submissions` |

## Module: MoodleGrades

| Fonction | Permission Moodle requise |
|----------|---------------------------|
| `get_submissions()` | `mod_assign_get_submissions`, `mod_assign_get_grades` |
| `update_grades()` | `mod_assign_save_grade` |

## Module: MoodleUsers

| Fonction | Permission Moodle requise |
|----------|---------------------------|
| `create_user()` | `core_user_create_users` |
| `get_users()` | `core_user_get_users` |
| `update_users()` | `core_user_update_users` |

---

## Comment activer ces permissions dans Moodle

### 1. Via l'interface d'administration

1. Allez dans **Administration du site → Plugins → Services web → Gérer les services**
2. Créez un nouveau service ou éditez un service existant
3. Cliquez sur **Fonctions** pour ajouter les fonctions nécessaires
4. Pour chaque fonction listée ci-dessus, ajoutez-la au service

### 2. Via rôle personnalisé

1. **Administration du site → Utilisateurs → Permissions → Définir les rôles**
2. Créez un rôle "API User" avec les capacités suivantes :
   - `webservice/rest:use` - Utiliser le protocole REST
   - `moodle/webservice:createtoken` - Créer des tokens
3. Assignez ce rôle à l'utilisateur qui utilisera l'API

### 3. Génération du token

1. **Administration du site → Plugins → Services web → Gérer les tokens**
2. Créez un token pour l'utilisateur et le service configuré
3. Copiez le token généré dans votre fichier `.env`

---

## Configuration minimale pour MoodleGrader

Pour l'application **MoodleGrader**, ces permissions sont **obligatoires** :

```text
✅ core_webservice_get_site_info
✅ core_enrol_get_users_courses
✅ core_enrol_get_enrolled_users
✅ core_group_get_course_groups
✅ core_group_get_group_members
✅ mod_assign_get_assignments
✅ mod_assign_get_submissions
✅ mod_assign_get_grades
```

### Commandes SQL pour vérifier les permissions (optionnel)

```sql
-- Vérifier les fonctions disponibles pour un service
SELECT externalfunctionsid, name 
FROM mdl_external_services_functions esf
JOIN mdl_external_functions ef ON esf.functionname = ef.name
WHERE serviceid = YOUR_SERVICE_ID;
```

---

## Moodle versions supportées

- **Moodle 3.9+** : Toutes les fonctions disponibles
- **Moodle 3.5-3.8** : Certaines fonctions peuvent être limitées
- **Moodle < 3.5** : Non supporté

Vérifiez votre version avec `moodle.get_site_info()['release']`.
