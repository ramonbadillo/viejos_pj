from jinja2 import Markup, evalcontextfilter, escape


def init_app(app):
    """Initialize a Flask application with custom filters."""
    app.jinja_env.filters['datetime'] = do_datetime
    app.jinja_env.filters['date'] = do_date
    app.jinja_env.filters['duration'] = do_duration

    # The nl2br filter uses the Jinja enviroment's context to determine
    # whether to autoscape
    app.jinja_env.filters['nl2br'] = evalcontextfilter(do_nl2br)


def do_datetime(dt, format=None):
    """Jinja template filter to format a datetime object.
    >>> do_datetime(None)
    ''
    >>> from datetime import datetime
    >>> do_datetime(datetime(2014, 01, 23, 09, 00, 00))
    '2014-01-23 - Thursday at 9:00am'
    """

    if dt is None:
        # By default, render an empty string.
        return ''
    if format is None:
        # No format is given in the template call.
        # Use a default format.
        # No format is given in the template call.
        # Use a default format.
        #
        # Format time in its own strftime call in order to:
        # 1. Left-strip leading 0 in hour display.
        # 2. Use 'am'/'pm' (lower case) instead of 'AM'/'PM'.
        formatted_date = dt.strftime('%Y-%m-%d - %A')
        formatted_time =\
            dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = '%s at %s' %\
            (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted


def do_date(dt, format='%Y-%m-%d - %A'):
    """
    Jinja template filter to format a datetime object with date only.
    >>> do_date(None)
    ''
    >>> from datetime import datetime
    >>> do_date(datetime(2014, 01, 23, 09, 00, 00))
    '2014-01-23 - Thursday'
    """

    if dt is None:
        return ''
    # Only difference with do_datetime is the default format, but that is
    # convenient enough to warrant its own template filter.
    return dt.strftime(format)


def do_duration(seconds):
    """
    Jinja template filter to format seconds to humanized duration.
    >>> do_duration(60)
    '0 days, 0 hours, 1 minutes, 0 seconds'
    >>> do_duration(3600)
    '0 days, 1 hours, 0 minutes, 0 seconds'
    """

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    tokens = []
    tokens.append('{d} days')
    tokens.append('{h} hours')
    tokens.append('{m} minutes')
    tokens.append('{s} seconds')
    template = ', '.join(tokens)
    return template.format(d=d, h=h, m=m, s=s)


def do_nl2br(context, value):
    """
    Render newline \n characters as HTML line breaks <br />.

    By default, HTML normalizes all whitespace on display. This filter allows
    text with line breaks entered into a textarea input to later display in
    HTML with line breaks.

    The context argument is Jina's state for template rendering, wich
    includes configuraion. This filter inspects the context to determine
    wheter to auto-escape content, e.g. conver <script> to &lt;script&gt.
    """
    formatted = u'<br />'.join(escape(value).split('\n'))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted
