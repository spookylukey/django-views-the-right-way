# Quick and dirty URL checker:
#
# - checks presence of parameters to every callback registered in main urlconf
# - checks for bad additional parameters (args without default)
# - checks type of parameters if possible
#   - can handle all Django's built-in path converters,
#     and any other that has a type annotation on the `to_python` method
#
# Limitations
# - can't check callbacks defined using ``**kwargs`` (e.g. most CBVs)

# TODO
# - Fine-grained methods for silencing checks.
# - Should only warn for each unhandled Converter once
# - Regex patterns perhaps? (only RoutePattern supported at the moment)
# - Probably lots of bugs...

import uuid

from inspect import Parameter, signature

from django.conf import settings
from django.core.checks import Error, Tags, Warning, register
from django.urls import URLPattern, URLResolver, get_resolver
from django.urls.resolvers import RoutePattern
from django.urls import converters


@register(Tags.urls)
def check_url_signatures(app_configs, **kwargs):
    if not getattr(settings, 'ROOT_URLCONF', None):
        return []

    resolver = get_resolver()
    errors = []
    for route in get_all_routes(resolver):
        errors.extend(check_url_args_match(route))
    return errors


def get_all_routes(resolver):
    for pattern in resolver.url_patterns:
        if isinstance(pattern, URLResolver):
            yield from get_all_routes(pattern)
        else:
            if isinstance(pattern.pattern, RoutePattern):
                yield pattern


def check_url_args_match(url_pattern: URLPattern):
    callback = url_pattern.callback
    callback_repr = f'{callback.__module__}.{callback.__qualname__}'
    errors = []
    sig = signature(callback)
    parameters = sig.parameters

    has_star_args = False
    if any(p.kind in [Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL]
           for p in parameters.values()):
        errors.append(Warning(
            f'View {callback_repr} signature contains *args or **kwarg syntax, can\'t properly check args',
            obj=url_pattern,
            id='urlchecker.W001',
        ))
        has_star_args = True

    used_from_sig = []
    parameter_list = list(sig.parameters)
    if parameter_list and parameter_list[0] == 'self':
        # HACK: we need to find some nice way to detect closures/bound methods,
        # while also getting the final signature.
        parameter_list.pop(0)
        used_from_sig.append('self')

    if not parameter_list or parameter_list[0] != 'request':
        if not has_star_args:
            if parameter_list:
                message = (
                    f'View {callback_repr} signature does not start with `request` parameter, '
                    f'found `{parameter_list[0]}`.'
                )
            else:
                message = f'View {callback_repr} signature does not have `request` parameter.'
            errors.append(Error(
                message,
                obj=url_pattern,
                id='urlchecker.E001',
            ))
    else:
        used_from_sig.append('request')

    # Everything in RoutePattern must be in signature
    for name, converter in url_pattern.pattern.converters.items():
        if has_star_args:
            used_from_sig.append(name)
        elif name in sig.parameters:
            used_from_sig.append(name)
            expected_type = get_converter_output_type(converter)
            found_type = sig.parameters[name].annotation
            if expected_type == Parameter.empty:
                # TODO - only output this warning once per converter
                errors.append(Warning(
                    f'Don\'t know output type for convert {converter}, can\'t verify URL signatures.',
                    obj=converter,
                    id=f'urlchecker.W002.{converter.__module__}.{converter.__class__.__name__}',
                ))
            elif found_type == Parameter.empty:
                errors.append(Warning(
                    f'Missing type annotation for parameter `{name}`, can\'t check type.',
                    obj=url_pattern,
                    id='urlchecker.W003'
                ))
            elif expected_type != found_type:
                errors.append(Error(
                    f'For parameter `{name}`, annotated type {found_type.__name__} does not match'
                    f' expected `{expected_type.__name__}` from urlconf',
                    obj=url_pattern,
                    id='urlchecker.E002',
                ))
        else:
            errors.append(Error(
                f'View {callback_repr} signature does not contain `{name}` parameter',
                obj=url_pattern,
                id='urlchecker.E003',
            ))

    # Anything left over must have a default argument
    for name, param in sig.parameters.items():
        if name in used_from_sig:
            continue
        if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            continue
        if param.default == Parameter.empty:
            errors.append(Error(
                f'View {callback_repr} signature contains `{name}` parameter without default or ULRconf parameter',
                obj=url_pattern,
                id='urlchecker.E004',
            ))

    return errors


CONVERTER_TYPES = {
    converters.IntConverter: int,
    converters.StringConverter: str,
    converters.UUIDConverter: uuid.UUID,
    converters.SlugConverter: str,
    converters.PathConverter: str,
}


def get_converter_output_type(converter):
    cls = type(converter)
    if cls in CONVERTER_TYPES:
        return CONVERTER_TYPES[cls]

    sig = signature(converter.to_python)
    if sig.return_annotation != Parameter.empty:
        return sig.return_annotation

    return Parameter.empty
