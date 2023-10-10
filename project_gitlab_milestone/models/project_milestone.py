# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import api, fields, models, exceptions
import gitlab
from odoo.addons.project_gitlab_base.utilities.gitlab_auth import gitlab_auth


def _create_gitlab_milestone(milestone) -> None:
    gl = gitlab_auth(milestone)

    if not gl:
        return

    project_id = milestone.project_id.gitlab_project_id

    if not project_id:
        raise exceptions.UserError('Gitlab project ID not set. Failed to create Gitlab milestone.')

    project = gl.projects.get(project_id)

    if not project:
        raise exceptions.UserError('Gitlab project not found. Failed to create Gitlab milestone.')

    data = {
        'title': milestone.name,
        'due_date': milestone.target_date,
    }

    response = project.milestones.create(data)

    milestone.gitlab_milestone_id = response.id


def _update_gitlab_milestone(milestone) -> None:
    gl = gitlab_auth(milestone)

    if not gl:
        return

    project_id = milestone.project_id.gitlab_project_id

    if not project_id:
        raise exceptions.UserError('Gitlab project ID not set. Failed to update Gitlab milestone.')

    project = gl.projects.get(project_id)

    if not project:
        raise exceptions.UserError('Gitlab project not found. Failed to update Gitlab milestone.')

    try:
        gitlab_milestone = project.milestones.get(milestone.gitlab_milestone_id)
    except gitlab.exceptions.GitlabGetError:
        _create_gitlab_milestone(milestone)
        return

    gitlab_milestone.title = milestone.name
    gitlab_milestone.due_date = milestone.target_date

    gitlab_milestone.save()


def _delete_gitlab_milestone(milestone) -> None:
    gl = gitlab_auth(milestone)

    if not gl:
        return

    project_id = milestone.project_id.gitlab_project_id

    if not project_id:
        raise exceptions.UserError('Gitlab project ID not set. Failed to delete Gitlab milestone.')

    project = gl.projects.get(project_id)

    if not project:
        raise exceptions.UserError('Gitlab project not found. Failed to delete Gitlab milestone.')

    try:
        gitlab_milestone = project.milestones.get(milestone.gitlab_milestone_id)
        gitlab_milestone.delete()
    except gitlab.exceptions.GitlabGetError:
        raise exceptions.UserError('Gitlab milestone not found')


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    gitlab_milestone_id = fields.Integer(string="Gitlab Milestone ID")

    @api.model
    def create(self, vals):
        milestone = super().create(vals)

        if not milestone.project_id.gitlab_enabled:
            return milestone

        _create_gitlab_milestone(milestone)

        return milestone

    @api.model
    def write(self, vals):
        result = super().write(vals)

        for milestone in self:
            if not milestone.project_id.gitlab_enabled:
                continue

            if 'name' in vals or 'target_date' in vals:
                _update_gitlab_milestone(milestone)

        return result

    @api.model
    def unlink(self):
        for milestone in self:
            if not milestone.project_id.gitlab_enabled:
                continue

            _delete_gitlab_milestone(milestone)

        return super().unlink()
