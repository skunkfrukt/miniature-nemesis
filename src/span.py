CELL_WIDTH = 20
CELL_HEIGHT = 20


class Placeholder(object):
    """
    Holds the type, coordinates and parameters of an object to be spawned
    later.
    ##IDEA## Add optional probability argument to Placeholder.
    """

    def __init__(self, object_type, x, y, **kwargs):
        self.object_type = object_type
        self.x, self.y = x, y
        self.kwargs = kwargs

    @attribute
    def width(self):
        return self.object_type.width

    @attribute
    def height(self):
        return self.object_type.height

    @attribute
    def left(self):
        return self.x

    @attribute
    def right(self):
        return self.x + self.width

    @attribute
    def bottom(self):
        return self.y

    @attribute
    def top(self):
        return self.y + self.height


class AmbushPlaceholder(Placeholder):
    """
    A Placeholder to be placed outside the left edge of the screen.
    """

    def __init__(self, object_type, x, y, **kwargs):
        self.object_type = object_type
        self.x = x - self.width  # This is basically what sets it apart.
        self.y = y
        self.kwargs = kwargs


class Span(object):
    """
    A single section of a Stage, containing Placeholder objects and logic to
    prevent overlap.
    The vanilla Span class is used for static, usually unique, sections into
    which each Placeholder needs to be put manually. Subclasses will handle
    procedural content to add some variety to repeated features.
    ##IDEA## BGM to be set on a Span basis.
    """

    def __init__(self, width, height, **kwargs):
        assert len(kwargs) == 0, 'Extra kwargs passed to Span: {}'.format(
                kwargs.keys())
        assert width > 0 and height > 0, 'Invalid Span dimensions: {}'.format(
                (width, height))

        self.width = width
        self.height = height
        self.cells = set([(x, y) for x in range(0, self.width, CELL_WIDTH)
                for y in range(0, self.height, CELL_HEIGHT)])
        self.content = []

    def add(self, placeholder):
        footprint = calculate_footprint(placeholder)
        if footprint in self.cells:
            self._add_placeholder(placeholder, footprint)
        else:
            pass  ##TODO## Raise an error: Object does not fit.

    def calculate_footprint(self, placeholder):
        if placeholder.right < 0:
            return set()
        start_x = placeholder.left - (placeholder.left % CELL_WIDTH)
        end_x = placeholder.right

        if placeholder.bottom < 0:
            start_y = 0
        else:
            start_y = placeholder.left - (placeholder.left % CELL_HEIGHT)
        end_y = min(placeholder.right, self.height)

        footprint = set([(x, y) for x in range(start_x, end_x, CELL_WIDTH)
                for y in range(start_y, end_y, CELL_HEIGHT)])
        return footprint

    def _add_placeholder(self, placeholder, footprint):
        self.content.append(placeholder)
        self.cells -= footprint

    def _sort_placeholders(self):
        self.content.sort(key=self._get_placeholder_sort_key)

    def _get_placeholder_sort_key(self, placeholder):
        """Sorts by x coordinate, but puts negative numbers last."""
        x = placeholder.x
        if x < 0:
            return self.width
        else:
            return x


class Stage(object):
    """
    A playable level of the game, consisting of a number of Span objects.
    """

    def __init__(self):
        self.spans = []
        self.width = 0
        self.offset = 0

    def add_span(self, span):
        self.spans.append(span)
        self.width += span.width
