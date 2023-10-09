# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    gitlab_enabled = fields.Boolean(string='Use Gitlab in project', default=False, track_visibility="onchange")
    gitlab_url = fields.Char(string='Gitlab URL', default='https://gitlab.com', track_visibility="onchange")
    gitlab_token = fields.Char(string='Gitlab Token', track_visibility="onchange")
    gitlab_project_id = fields.Char(string='Gitlab Project ID', track_visibility="onchange")
