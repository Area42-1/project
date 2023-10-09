# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    gitlab_commit_ids = fields.One2many(
        comodel_name='project.gitlab.history',
        inverse_name='task_id',
        string='Gitlab Commits'
    )
