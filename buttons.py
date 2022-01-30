class Button:
    def __init__(self, button):
        # Button object
        self.button = button
        # Track down/up event
        self.was_pressed = False
        # Currently down
        self.is_down = False
        # Extra latch to opt out of a press
        self.latched = False

    # Update states
    def poll(self):
        # Get current state
        down = not self.button.value
        # Don't change states if we were pressed
        if not self.was_pressed:
            # If was down but now not
            if self.is_down and not down:
                # Mark pressed unless latched
                self.was_pressed = True if not self.latched else False
                # And released
                self.is_down = False
                # And unlatch
                self.latched = False
            # Else if new down state
            elif down:
                # Mark it
                self.is_down = True

    def latch(self):
        self.latched = True

    @property
    def down(self):
        # Return down-but-not-pressed
        return self.is_down

    @property
    def pressed(self):
        # If we were pressed
        if self.was_pressed:
            # Clear state and return press
            self.was_pressed = False
            return True
        # Else false
        else:
            return False

class Buttons:
    def __init__(self, buttons):
        self.buttons = []
        for b in buttons:
            self.buttons.append(Button(b))

    # Poll button states
    def poll(self):
        for b in self.buttons:
            b.poll()

    # Any currently down?
    @property
    def down(self):
        return any(map(lambda b:b.is_down, self.buttons))

    @property
    def pressed(self):
        return any(map(lambda b:b.was_pressed, self.buttons))

    def __getitem__(self, index):
        return self.buttons[index]