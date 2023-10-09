# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import http
from odoo.http import request
from datetime import datetime, timezone


class Main(http.Controller):
    @http.route('/gitlab/webhook', type='json', auth='none', methods=['POST'], csrf=False)
    def gitlab_webhook_handler(self, **kwargs):
        event: str = request.httprequest.headers.get('X-Gitlab-Event')
        token: str = request.httprequest.headers.get('X-Gitlab-Token')

        if token != request.env["ir.config_parameter"].sudo().get_param("project_gitlab.display_x_gitlab_token"):
            return 'Invalid token'

        if event == 'Push Hook':
            return self._handle_push_event(request)
        elif event == 'Merge Request Hook':
            return self._handle_merge_request_event(request)
        else:
            return 'Event not handled'

    def _handle_push_event(self, request) -> str:
        data = request.jsonrequest

        project = data.get('project', [])

        project = request.env['project.project'].sudo().search([('gitlab_project_id', '=', project.get('id'))], limit=1)

        if not project:
            return "No project found"

        commits = data.get('commits', [])

        if not commits:
            return "No commit found"

        for commit in commits:
            task_code = commit.get('message').split(':')[0].split(' ')[0]
            if task_code == 'Merge':
                continue

            task = request.env['project.task'].sudo().search([('key', '=', task_code)], limit=1)

            if not task:
                continue

            event_type = data.get('event_name')

            date = (datetime.fromisoformat(commit.get('timestamp'))
                    .astimezone(timezone.utc)
                    .strftime('%Y-%m-%d %H:%M:%S'))

            data = {
                'project_id': project.id,
                'task_id': task.id,
                'commit_id': commit.get('id'),
                'event_type': event_type.capitalize(),
                'date': date,
                'content': commit.get('message'),
                'url': commit.get('url'),
            }

            self._add_history(data)

        return "Push event handled"

    def _handle_merge_request_event(self, request) -> str:
        data = request.jsonrequest

        project = data.get('project', [])

        if not project:
            return "No project found"

        project = request.env['project.project'].sudo().search([('gitlab_project_id', '=', project.get('id'))], limit=1)

        if not project:
            return "No project found"

        object_attributes = data.get('object_attributes', [])

        if not object_attributes:
            return "No object attributes found"

        source_branch = object_attributes.get('source_branch')
        task_code = source_branch.split('/')[1]

        task = request.env['project.task'].sudo().search([('key', '=', task_code)], limit=1)

        if not task:
            return "No task found"

        event_type = data.get('event_type').replace('_', ' ').capitalize()

        date = (datetime.strptime(object_attributes.get('created_at'), '%Y-%m-%d %H:%M:%S %Z')
                .strftime('%Y-%m-%d %H:%M:%S'))

        data = {
            'project_id': project.id,
            'task_id': task.id,
            'commit_id': object_attributes.get('merge_commit_sha'),
            'event_type': event_type,
            'date': date,
            'content': object_attributes.get('title'),
            'url': object_attributes.get('url'),
        }

        self._add_history(data)

        return "Merge request event handled"

    def _add_history(self, data):
        request.env['project.gitlab.history'].sudo().create(data)
