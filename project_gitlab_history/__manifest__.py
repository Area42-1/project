# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    "name": "Gitlab Project History Connector",
    "summary": "Gitlab history connector for projects",
    "version": "14.0.1.0.0",
    "category": "Project Management",
    "author": "Kévin Allard",
    "license": "AGPL-3",
    "depends": ["project", "project_key", "project_gitlab_base"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task_view.xml",
    ]
}
