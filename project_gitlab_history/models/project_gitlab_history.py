# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import fields, models


class GitlabCommit(models.Model):
    _name = 'project.gitlab.history'
    _description = 'Gitlab History'
    _order = 'date DESC'

    project_id = fields.Many2one(comodel_name='project.project', string='Project', required=True)
    task_id = fields.Many2one(comodel_name='project.task', string='Task', required=True)
    commit_id = fields.Char(string='Commit ID', required=True)
    event_type = fields.Char(string='Event Type', required=True)
    date = fields.Datetime(string='Date', required=True)
    content = fields.Text(string='content', required=True)
    url = fields.Char(string='URL', required=True)
