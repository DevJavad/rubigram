#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import Optional, TypeVar, Union, Type, get_type_hints, get_origin, get_args
from dataclasses import fields
from json import dumps
import sys
import rubigram


T = TypeVar("T", bound="Object")


class Object:
    """
    Base class for all Rubigram data objects.

    Provides core features for:
    - Client binding to nested objects.
    - Serialization to dict or JSON.
    - Parsing from dictionaries into typed instances.
    """

    def bind(
        self,
        client: "rubigram.Client"
    ) -> None:
        """Bind a client instance to this object and all nested Object instances.

        This method recursively attaches a Rubigram client to the current object
        and all its nested `Object` instances. It allows method calls within objects
        (e.g., `message.reply()`) to access the bound client.

        Args:
            client (rubigram.Client): The client instance to bind to this object.
        """

        object.__setattr__(self, "client", client)
        for field in fields(self):
            value = getattr(self, field.name)

            if isinstance(value, Object):
                value.bind(client)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Object):
                        item.bind(client)

    def as_dict(self):
        """Convert this object into a dictionary representation.

        Converts the current object and all nested `Object` instances into
        a serializable dictionary that includes type information.

        Returns:
            dict: A dictionary representation of this object.
        """

        data = {}

        for field in fields(self):
            value = getattr(self, field.name)

            if isinstance(value, Object):
                inner = value.as_dict()
                data[field.name] = {"_": value.__class__.__name__, **inner}

            elif isinstance(value, list):
                data[field.name] = [
                    {"_": v.__class__.__name__, **v.as_dict()} if isinstance(v,
                                                                             Object) else v
                    for v in value
                ]

            else:
                data[field.name] = value

        return data

    def jsonify(
        self,
        exclude_none: bool = True
    ) -> str:
        """Convert this object into a JSON string.

        Serializes the current object and all nested `Object` instances into a
        human-readable JSON string. Optionally removes all `None` values.

        Args:
            exclude_none (bool, optional): Whether to remove `None` values from the output.
                Defaults to True.

        Returns:
            str: A formatted JSON string representation of this object.
        """

        def clear(object):
            if isinstance(object, dict):
                return {
                    key: clear(value) for key, value in object.items() if value is not None
                }

            elif isinstance(object, list):
                return [
                    clear(item) for item in object if item is not None
                ]

            else:
                return object

        data = self.as_dict()

        if exclude_none:
            data = clear(data)

        return dumps({
            "_": self.__class__.__name__, **data
        }, ensure_ascii=False, indent=4, default=str)

    @classmethod
    def parse(
        cls: Type[T],
        data: dict,
        client: Optional["rubigram.Client"] = None
    ) -> T:
        """Parse a dictionary into an instance of this Object subclass.

        Converts raw API data or serialized dictionaries into fully-typed
        Rubigram objects, including nested objects and lists.

        Args:
            data (dict): The source dictionary to parse.
            client (rubigram.Client, optional): Optional client instance to bind to
                the parsed object and all nested objects.

        Returns:
            T: A new instance of the class populated with parsed data.
        """

        if not data:
            object = cls()
            if client is not None:
                object.bind(client)
            return object

        data = {
            key: value for key, value in data.items() if key != "_"
        }
        init_data = {}

        try:
            module = sys.modules[cls.__module__]
            type_hints = get_type_hints(cls, globalns=module.__dict__)

        except:
            type_hints = {}

        for field in fields(cls):
            raw_value = data.get(field.name)
            field_type = type_hints.get(field.name, field.type)
            origin = get_origin(field_type)

            if isinstance(raw_value, dict) and "_" in raw_value:
                raw_value = {
                    key: value for key, value in raw_value.items() if key != "_"
                }

            elif origin is list and isinstance(raw_value, list):
                inner_type = get_args(field_type)[0]

                if hasattr(inner_type, "__origin__"):
                    non_none = [
                        t for t in get_args(inner_type) if t is not type(None)
                    ]
                    inner_type = non_none[0] if non_none else inner_type

                if isinstance(inner_type, type) and issubclass(inner_type, Object):
                    init_data[field.name] = [
                        inner_type.parse(value, client) if isinstance(
                            value, dict) else value
                        for value in raw_value
                    ]

                else:
                    init_data[field.name] = raw_value

            elif origin is Union and isinstance(raw_value, dict):
                args = [
                    arg for arg in get_args(field_type) if arg is not type(None)
                ]
                object_type = next(
                    (
                        arg for arg in args if isinstance(arg, type) and issubclass(arg, Object)
                    ), None
                )

                if object_type:
                    init_data[field.name] = object_type.parse(
                        raw_value, client)

                else:
                    init_data[field.name] = raw_value

            else:
                init_data[field.name] = raw_value

        object = cls(**init_data)

        if client is not None:
            object.bind(client)

        return object

    def __str__(self):
        """Return a readable string representation of this object.

        Returns:
            str: JSON-formatted string of this object for debugging or logging.
        """

        return self.jsonify()