from odoo.exceptions import UserError
import gitlab


def gitlab_auth(data) -> gitlab.Gitlab:
    url: str = data.project_id.gitlab_url
    token: str = data.project_id.gitlab_token

    if not url:
        raise UserError('Gitlab URL not set. Failed to create Gitlab milestone.')

    if not token:
        raise UserError('Gitlab token not set. Failed to create Gitlab milestone.')

    gl = gitlab.Gitlab(url, private_token=token)
    gl.auth()

    return gl
