from kivy.properties import BooleanProperty, ObjectProperty
from kivy.core.window import Window


class HoverBehavior(object):
    """
    :Events:
        :attr:`on_enter`
            Fired when mouse enter the bbox of the widget.
        :attr:`on_leave`
            Fired when the mouse exit the widget.
    """

    hovered = BooleanProperty(False)
    """
    `True`, if the mouse cursor is within the borders of the widget.

    :attr:`hovered` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    border_point = ObjectProperty(None)
    """Contains the last relevant point received by the Hoverable.
    This can be used in :attr:`on_enter` or :attr:`on_leave` in order
    to know where was dispatched the event.

    :attr:`border_point` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    def __init__(self, **kwargs):
        self.register_event_type("on_enter")
        self.register_event_type("on_leave")
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            # We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch("on_enter")
        else:
            self.dispatch("on_leave")

    def on_enter(self):
        """Fired when mouse enter the bbox of the widget."""

    def on_leave(self):
        """Fired when the mouse exit the widget."""


from kivy.factory import Factory

Factory.register("HoverBehavior", HoverBehavior)
