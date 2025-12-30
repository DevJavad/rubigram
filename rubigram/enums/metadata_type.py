#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from .enum import Enum


class MetadataType(Enum):
    BOLD = "Bold"
    MONO = "Mono"
    LINK = "Link"
    QUOTE = "Quote"
    ITALIC = "Italic"
    STRIKE = "Strike"
    SPOILER = "Spoiler"
    UNDERLINE = "Underline"
    MENTION_TETX = "MentionText"