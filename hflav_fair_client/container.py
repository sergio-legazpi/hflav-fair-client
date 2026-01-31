from dependency_injector import containers, providers

from hflav_fair_client.cache import init_cache
from hflav_fair_client.conversors.template_schema_handler import TemplateSchemaHandler
from hflav_fair_client.conversors.dynamic_conversor import DynamicConversor
from hflav_fair_client.conversors.gitlab_schema_handler import GitlabSchemaHandler
from hflav_fair_client.conversors.zenodo_schema_handler import ZenodoSchemaHandler
from hflav_fair_client.filters.zenodo_query import ZenodoQuery
from hflav_fair_client.processing.data_visualizer import DataVisualizer
from hflav_fair_client.services.command import CommandInvoker
from hflav_fair_client.services.service import (
    Service,
)
from hflav_fair_client.source.source_gitlab_client import SourceGitlabClient
from hflav_fair_client.source.source_zenodo_random_data import SourceZenodoRandomData
from hflav_fair_client.source.source_zenodo_requests import SourceZenodoRequest


class Container(containers.DeclarativeContainer):
    """Dependency injection container for HFLAV FAIR client library."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "hflav_fair_client.conversors.conversor_handler",
            "hflav_fair_client.conversors.zenodo_schema_handler",
            "hflav_fair_client.conversors.gitlab_schema_handler",
            "hflav_fair_client.services.service",
            "hflav_fair_client.conversors.dynamic_conversor",
            "hflav_fair_client.filters.search_filters",
            "hflav_fair_client.models.hflav_data_searching",
        ]
    )

    _cache = providers.Resource(init_cache)

    source = providers.Singleton(SourceZenodoRequest)
    gitlab_source = providers.Singleton(SourceGitlabClient)
    conversor = providers.Singleton(DynamicConversor)
    visualizer = providers.Singleton(DataVisualizer)
    command_invoker = providers.Singleton(CommandInvoker)
    base_query = providers.Callable(lambda: ZenodoQuery)

    zenodo_schema_handler = providers.Factory(
        ZenodoSchemaHandler, source=source, conversor=conversor, visualizer=visualizer
    )

    gitlab_schema_handler = providers.Factory(
        GitlabSchemaHandler, source=source, conversor=conversor, visualizer=visualizer
    )

    template_schema_handler = providers.Factory(
        TemplateSchemaHandler, source=source, conversor=conversor, visualizer=visualizer
    )
    handler_schema_chain = providers.Callable(
        lambda zh, gh, th: (
            zh.set_next(gh),
            gh.set_next(th),
            zh,
        )[-1],
        zh=zenodo_schema_handler,
        gh=gitlab_schema_handler,
        th=template_schema_handler,
    )

    service = providers.Factory(
        Service,
        source=source,
        conversor=conversor,
        command_invoker=command_invoker,
        handler_schema_chain=handler_schema_chain,
    )
