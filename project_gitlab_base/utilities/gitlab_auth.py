from odoo import api, fields, models, exceptions
import gitlab


def gitlab_auth(milestone) -> gitlab.Gitlab:
    url: str = milestone.project_id.gitlab_url
    token: str = milestone.project_id.gitlab_token

    if not url:
        raise exceptions.UserError('Gitlab URL not set. Failed to create Gitlab milestone.')

    if not token:
        raise exceptions.UserError('Gitlab token not set. Failed to create Gitlab milestone.')

    gl = gitlab.Gitlab(url, private_token=token)
    gl.auth()

    return gl
