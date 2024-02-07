# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    gitlab_enabled = fields.Boolean(string='Use Gitlab in project', default=False, tracking=True)
    gitlab_url = fields.Char(string='Gitlab URL', default='https://gitlab.com', tracking=True)
    gitlab_token = fields.Char(string='Gitlab Token', tracking=True)
    gitlab_project_id = fields.Char(string='Gitlab Project ID', tracking=True)


class ProjectType(models.Model):
    _inherit = 'project.type'

    gitlab_enabled = fields.Boolean(string='Use Gitlab in project', default=False, tracking=True)
    gitlab_url = fields.Char(string='Gitlab URL', default='https://gitlab.com', tracking=True)
    gitlab_token = fields.Char(string='Gitlab Token', tracking=True)
    gitlab_project_id = fields.Char(string='Gitlab Project ID', tracking=True)
