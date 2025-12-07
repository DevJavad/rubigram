from rubigram.types import Keypad, KeypadRow, Button


def user_count(user: int) -> "Keypad":
    return Keypad(
        [
            KeypadRow(
                [
                    Button("user", "number of users bot: {}".format(user))
                ]
            )
        ]
    )