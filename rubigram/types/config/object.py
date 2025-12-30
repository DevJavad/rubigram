#  RubigramClient - Rubika API library for python
#  Copyright (C) 2025-present Javad <https://github.com/DevJavad>
#  Github - https://github.com/DevJavad/rubigram


from typing import (
    Optional,
    TypeVar,
    Union,
    Type,
    Any,
    get_type_hints,
    get_origin,
    get_args
)
from dataclasses import fields
from json import dumps
import sys
import rubigram


T = TypeVar("T", bound="Object")


FIELDS_CACHE: dict[type, tuple] = {}
TYPE_HINTS_CACHE: dict[type, dict] = {}


def get_fields(cls: type):
    """
    Get cached dataclass fields for a class.

    This function caches the result of `dataclasses.fields()` to avoid
    repeated computation for the same class.

    Parameters:
        cls (type):
            The dataclass type to get fields for.

    Returns:
        tuple[Field]: A tuple of field objects for the dataclass.

    Example:
    .. code-block:: python
        fields = get_fields(User)
        for field in fields:
            print(field.name, field.type)
    """
    cached = FIELDS_CACHE.get(cls)
    if cached is None:
        cached = fields(cls)
        FIELDS_CACHE[cls] = cached
    return cached


def get_cached_type_hints(cls: type) -> dict:
    """
    Get cached type hints for a class.

    This function retrieves and caches type annotations for a class,
    respecting the module's global namespace for forward references.

    Parameters:
        cls (type):
            The class to get type hints for.

    Returns:
        dict[str, type]: A dictionary mapping field names to their types.

    Note:
        If type hints cannot be retrieved (e.g., due to forward references
        in a different module), an empty dictionary is returned and cached.

    Example:
    .. code-block:: python
        hints = get_cached_type_hints(User)
        print(hints["user_id"])  # <class 'int'>
    """
    cached = TYPE_HINTS_CACHE.get(cls)
    if cached is None:
        try:
            module = sys.modules[cls.__module__]
            cached = get_type_hints(cls, globalns=module.__dict__)
        except Exception:
            cached = {}
        TYPE_HINTS_CACHE[cls] = cached
    return cached


def strip_optional(tp):
    """
    Extract the non-None type from an Optional annotation.

    Given a Union type (typically from Optional[T]), returns T.
    If no non-None type is found, returns the original type.

    Parameters:
        tp (type):
            The type annotation, e.g., Optional[int] or Union[int, None].

    Returns:
        type: The non-None type from the union, or the original type.

    Example:
    .. code-block:: python
        t = strip_optional(Optional[int])  # returns <class 'int'>
        t = strip_optional(Union[int, str, None])  # returns <class 'int'>
    """
    for arg in get_args(tp):
        if arg is not type(None):
            return arg
    return tp


def is_object_type(tp) -> bool:
    """
    Check if a type is a subclass of Object.

    Parameters:
        tp (type):
            The type to check.

    Returns:
        bool: True if tp is a class and subclass of Object, False otherwise.

    Example:
    .. code-block:: python
        is_object_type(User)  # True if User extends Object
        is_object_type(int)   # False
    """
    return isinstance(tp, type) and issubclass(tp, Object)


def clear_none(data: Any):
    """
    Recursively remove None values from dictionaries and lists.

    This function deeply traverses nested structures and removes:
    - Keys with None values from dictionaries
    - None items from lists

    Parameters:
        data (Any):
            The data structure to clean. Can be dict, list, or any other type.

    Returns:
        Any: The cleaned data structure with None values removed.

    Note:
        Returns non-dict/list values unchanged.

    Example:
    .. code-block:: python
        data = {"a": 1, "b": None, "c": [1, None, {"d": None}]}
        cleaned = clear_none(data)
        # Result: {"a": 1, "c": [1, {}]}
    """
    if isinstance(data, dict):
        return {
            key: clear_none(value)
            for key, value in data.items()
            if value is not None
        }
    if isinstance(data, list):
        return [
            clear_none(i)
            for i in data
            if i is not None
        ]
    return data


class Object:
    """
    Base class for all API data models in Rubigram.

    This class provides serialization, deserialization, and client binding
    functionality for dataclass-based models. It handles complex type
    annotations including Optional, List, and nested Object types.

    The class is designed to work with Rubika API responses, automatically
    parsing JSON data into Python objects and vice versa.

    Attributes:
        client (Optional[rubigram.Client]):
            The client instance bound to this object. Used for making
            subsequent API calls from within the object context.

    Slots:
        __slots__ = ("client",): Optimizes memory usage by restricting
            dynamic attribute creation.

    Example:
    .. code-block:: python
        @dataclass
        class User(Object):
            user_id: int
            name: str
            profile: Optional[Profile] = None

        # Parse from API response
        user = User.parse({"user_id": 123, "name": "John"})

        # Serialize to JSON
        json_str = user.jsonify()

        # Bind to client for API operations
        user.bind(client)
    """

    __slots__ = ("client",)

    def bind(self, client: "rubigram.Client") -> None:
        """
        Bind a client instance to this object and all nested Object instances.

        This method recursively traverses the object's fields and binds the
        client to any nested Object instances or lists containing Objects.

        Parameters:
            client (rubigram.Client):
                The client instance to bind.

        Returns:
            None

        Note:
            The client is stored using `object.__setattr__` to bypass
            the restrictions of `__slots__`.

        Example:
        .. code-block:: python
            user.bind(client)
            # Now user and all nested objects can use client for API calls
        """
        object.__setattr__(self, "client", client)

        for field in get_fields(self.__class__):
            value = getattr(self, field.name)

            if isinstance(value, Object):
                value.bind(client)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, Object):
                        item.bind(client)

    def as_dict(self) -> dict:
        """
        Convert the object to a dictionary representation suitable for JSON serialization.

        Returns:
            dict: A dictionary where:
                - Object instances are converted to dict with "_" type marker
                - Lists are recursively processed
                - Simple values are included as-is

        Note:
            This method adds a "_" key with the class name for Object instances,
            matching Rubika API's type indicator convention.

        Example:
        .. code-block:: python
            user = User(user_id=123, name="John")
            data = user.as_dict()
            # Result: {"user_id": 123, "name": "John"}

            profile = Profile(avatar="url")
            user.profile = profile
            data = user.as_dict()
            # Result: {"user_id": 123, "name": "John", 
            #          "profile": {"_": "Profile", "avatar": "url"}}
        """
        result = {}

        for field in get_fields(self.__class__):
            value = getattr(self, field.name)

            if isinstance(value, Object):
                result[field.name] = {
                    "_": value.__class__.__name__,
                    **value.as_dict()
                }

            elif isinstance(value, list):
                result[field.name] = [
                    (
                        {"_": v.__class__.__name__, **v.as_dict()}
                        if isinstance(v, Object)
                        else v
                    )
                    for v in value
                ]

            else:
                result[field.name] = value

        return result

    def jsonify(self, exclude_none: bool = True) -> str:
        """
        Serialize the object to a JSON string.

        Parameters:
            exclude_none (bool, optional):
                If True (default), removes None values from the output.
                If False, includes None values in the JSON.

        Returns:
            str: A formatted JSON string with:
                - ASCII characters preserved
                - 4-space indentation
                - Type marker "_" included

        Note:
            Uses `default=str` to handle non-serializable types by
            converting them to strings.

        Example:
        .. code-block:: python
            user = User(user_id=123, name="John", profile=None)
            json_str = user.jsonify()
            # Result: '{"_": "User", "user_id": 123, "name": "John"}'

            json_str = user.jsonify(exclude_none=False)
            # Result: '{"_": "User", "user_id": 123, "name": "John", "profile": null}'
        """
        data = self.as_dict()

        if exclude_none:
            data = clear_none(data)

        return dumps(
            {"_": self.__class__.__name__, **data},
            ensure_ascii=False,
            indent=4,
            default=str
        )

    @classmethod
    def parse(cls: Type[T], data: dict, client: Optional["rubigram.Client"] = None) -> T:
        """
        Parse a dictionary (typically from JSON API response) into an Object instance.

        This is the primary factory method for creating Object instances from
        Rubika API responses. It handles:
        - Type conversion based on field annotations
        - Nested Object parsing
        - Optional and List type handling
        - Client binding

        Parameters:
            data (dict):
                The dictionary data to parse, typically from `response.json()`.
            client (Optional[rubigram.Client], optional):
                Client instance to bind to the created object and its children.

        Returns:
            T: An instance of the calling class, populated with data.

        Raises:
            TypeError: If data cannot be parsed according to field types.
            KeyError: If required fields are missing (depending on dataclass defaults).

        Note:
            - The "_" key (type marker) is automatically stripped from input data
            - For lists of Objects, each item is parsed recursively
            - Missing fields are set to None

        Example:
        .. code-block:: python
            json_data = {
                "_": "User",
                "user_id": 123,
                "name": "John",
                "profile": {"_": "Profile", "avatar": "url"}
            }
            user = User.parse(json_data, client=my_client)
            print(user.user_id)  # 123
            print(user.profile.avatar)  # "url"
        """
        if not data:
            obj = cls()
            if client:
                obj.bind(client)
            return obj

        data = {key: value for key, value in data.items() if key != "_"}
        init_data = {}

        fields_ = get_fields(cls)
        type_hints = get_cached_type_hints(cls)

        for field in fields_:
            raw = data.get(field.name)

            if raw is None:
                init_data[field.name] = None
                continue

            field_type = type_hints.get(field.name, field.type)
            origin = get_origin(field_type)

            if isinstance(raw, dict) and "_" in raw:
                raw = {k: v for k, v in raw.items() if k != "_"}

            if origin is list and isinstance(raw, list):
                inner = get_args(field_type)[0]
                inner_origin = get_origin(inner)

                if inner_origin is Union:
                    inner = strip_optional(inner)

                if is_object_type(inner):
                    init_data[field.name] = [
                        inner.parse(v, client) if isinstance(v, dict) else v
                        for v in raw
                    ]
                else:
                    init_data[field.name] = raw

            elif origin is Union:
                inner = strip_optional(field_type)

                if is_object_type(inner) and isinstance(raw, dict):
                    init_data[field.name] = inner.parse(raw, client)
                else:
                    init_data[field.name] = raw

            else:
                init_data[field.name] = raw

        obj = cls(**init_data)

        if client:
            obj.bind(client)

        return obj

    def __str__(self) -> str:
        return self.jsonify()