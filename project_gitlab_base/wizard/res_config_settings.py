# Copyright 2023 - present kallard <contact@area42.fr>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    project_display_x_gitlab_token = fields.Char(
        string='X-Gitlab-Token',
        config_parameter='project_gitlab.display_x_gitlab_token',
        help=(
            "Used to validate received payloads. Sent with the request in the X-Gitlab-Token HTTP header."
        ),
    )
