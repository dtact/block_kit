def wrap(cls):
    _old_new = cls.__new__
    _old_init = cls.__init__

    def __new__(cls_, *args, **kwargs):
        if issubclass(cls, str):
            d = args[0]
            if d is None:
                return
            elif type(d) is str:
                pass
            elif type(d) is int:
                d = str(d)
            else:
                raise Exception(f"{type(d)} not accepted for type {cls}")

            obj = _old_new(cls, d)
            return obj
        elif issubclass(cls, int):
            d = args[0]
            if d is None:
                return
            elif type(d) is str:
                d = int(d)
            elif type(d) is int:
                pass
            else:
                raise Exception(f"{type(d)} not accepted for type {cls}")

            obj = _old_new(cls, d)
            return obj
        elif issubclass(cls, list):
            allowed_types = cls._allowed_types

            d = []

            for arg in args:
                if arg is None:
                    continue
                elif type(arg) is dict and not arg:
                    # empty dict
                    continue
                elif type(arg) is list and not arg:
                    # empty dict
                    continue

                allowed = False

                for t in allowed_types:
                    if type(arg) is t:
                        allowed = True

                        d.append(arg)

                if not allowed:
                    raise Exception(
                        f"Type {type(arg)}({arg}) not supported for {cls}, allowed are: {allowed_types}"
                    )

            if not d:
                return None

            obj = _old_new(cls, d)
            _old_init(obj, d)
            return obj  # or d

        elif issubclass(cls, dict):
            allowed_types = cls._allowed_types

            d = {}

            for arg in args:
                if arg is None:
                    continue
                elif type(arg) is dict and not arg:
                    # empty dict
                    continue
                elif type(arg) is list and not arg:
                    # empty dict
                    continue

                allowed = False

                for (k, t) in allowed_types.items():
                    if type(t) is list:
                        for t2 in t:
                            if type(arg) is t2:
                                allowed = True

                                d[k] = arg
                    elif type(t) is str:
                        allowed = True
                        d[k] = t
                    else:
                        if type(arg) is t:
                            allowed = True

                            d[k] = arg

                if not allowed:
                    raise Exception(
                        f"Type {type(arg)}({arg}) not supported for {cls}, \
                        allowed are: {allowed_types}"
                    )

            if not d:
                return None

            obj = _old_new(cls, d)
            _old_init(obj, d)
            return obj  # or d

    def __dummy_init__(self, *args, **kwargs):
        # we'll override the init, as it will
        # expect different arguments
        pass

    cls.__new__ = __new__
    cls.__init__ = __dummy_init__
    return cls


@wrap
class ImageURL(str):
    pass


@wrap
class AltText(str):
    pass


@wrap
class Image(dict):
    _allowed_types = {"image_url": ImageURL, "alt_text": AltText, "type": "image"}


class PlainText(dict):
    def __init__(self, text, emoji=True):
        super().__init__(
            {
                "text": text.strip(),
                "type": "plain_text",
                "emoji": emoji,
            },
        )


class MarkDown(dict):
    def __init__(self, text):
        super().__init__(
            {
                "text": text.strip(),
                "type": "mrkdwn",
            },
        )


@wrap
class Divider(dict):
    _allowed_types = {
        "type": "divider",
    }



@wrap
class Header(dict):
    _allowed_types = {"text": [PlainText, MarkDown, str], "type": "header"}


@wrap
class Action(str):
    pass


@wrap
class ActionId(str):
    pass


@wrap
class Value(str):
    pass


@wrap
class Fields(list):
    _allowed_types = [MarkDown, PlainText]

@wrap
class Section(dict):
    _allowed_types = {
        "text": [PlainText, MarkDown, str],
        "type": "section",
        "fields": Fields,
    }


@wrap
class Button(dict):
    _allowed_types = {
        "type": "button",
        "text": [PlainText, MarkDown, str],
        "value": Value,
        "action": Action,
        "action_id": ActionId,
    }


@wrap
class Elements(list):
    _allowed_types = [Button]


@wrap
class Actions(dict):
    _allowed_types = {"elements": Elements, "type": "actions"}

@wrap
class Blocks(list):
    _allowed_types = [Section, Divider, Image, Header, Actions]


@wrap
class Message(dict):
    _allowed_types = {"blocks": Blocks}
