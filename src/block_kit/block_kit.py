class Wrap:
    def __new__(cls, s):
        if s is None:
            return
        elif type(s) is str:
            pass
        elif type(s) is int:
            s = str(s)
        else:
            raise Exception(f"{type(s)} not accepted for type {cls}")

        return super(Wrap, cls).__new__(cls, s)


class WrapDict:
    def __new__(cls, *args, **kwargs):
        print(cls)
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

        if hasattr(cls, "_old_new"):
            print("OLDNEW")
            obj = cls._old_new(cls, d)
            return obj

        obj = super(WrapDict, cls).__new__(cls, d)
        # cls.__init__(obj, d)
        super(WrapDict, cls).__init__(obj, d)
        if hasattr(obj, "_old_init"):
            print("OLDINIT")
            obj._old_init(d)
        #    obj.__remco__(d)
        return obj

    def __init__(self, *args, **kwargs):
        pass


def wrapdict(cls):
    _old_init2 = cls.__init__
    _old_new2 = cls.__new__

    class cls(WrapDict, dict):
        _allowed_types = cls._allowed_types
        _old_init = _old_init2
        _old_new = _old_new2

        def __new__(cls, d):
            print("wrapdict new")
            return super().__new__(cls, d)

        def __init__(self, *args, **kwargs):
            # print("WRAPDICT", cls, _old_init)
            super().__init__(args, kwargs)
            # _old_init(args, kwargs)

    # cls.__init__ = cls()
    return cls


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


class ImageURL(Wrap, str):
    pass


class AltText(Wrap, str):
    pass


class Image(WrapDict, dict):
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


class Divider(WrapDict, dict):
    _allowed_types = {
        "type": "divider",
    }


class Header(WrapDict, dict):
    _allowed_types = {"text": [PlainText, MarkDown, str], "type": "header"}


class Action(Wrap, str):
    pass


class ActionId(Wrap, str):
    pass


class Value(Wrap, str):
    pass


@wrap
class Fields(list):
    _allowed_types = [MarkDown, PlainText]


class Section(WrapDict, dict):
    _allowed_types = {
        "text": [PlainText, MarkDown, str],
        "type": "section",
        "fields": Fields,
    }


@wrapdict
class Button(dict):
    _allowed_types = {
        "type": "button",
        "text": [PlainText, MarkDown, str],
        "value": Value,
        "action": Action,
        "action_id": ActionId,
    }

    def __new__(cls, d):
        print("NEW BUTTON")
        return super(dict, cls).__new__(
            {
                **d,
                "remco": "remco",
            }
        )


@wrap
class Elements(list):
    _allowed_types = [Button]


class Actions(WrapDict, dict):
    _allowed_types = {"elements": Elements, "type": "actions"}


@wrap
class Blocks(list):
    _allowed_types = [Section, Divider, Image, Header, Actions]


class Message(WrapDict, dict):
    _allowed_types = {"blocks": Blocks}
