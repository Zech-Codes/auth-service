from auth.app import templates


def render(template, **context):
    return templates.get_template(template).render(context)
