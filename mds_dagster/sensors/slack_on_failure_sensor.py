"""
Dagster Native Integration for sending out alerts
"""
import os
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    TypeVar,
)

import dagster_slack
from dagster import (
    FreshnessPolicySensorContext,
    RunFailureSensorContext,
    SensorDefinition,
)
from dagster_slack import make_slack_on_run_failure_sensor

# # Monkey patching: The original function
T = TypeVar("T", RunFailureSensorContext, FreshnessPolicySensorContext)


def custom_build_slack_blocks_and_text(
    context: T,
    text_fn: Callable[[T], str],
    blocks_fn: Optional[Callable[[T], List[Dict[Any, Any]]]],
    webserver_base_url: Optional[str],
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Monkey Patching the original funciton from Dagster
    """
    main_body_text = text_fn(context)
    blocks: List[Dict[Any, Any]] = []
    if blocks_fn:
        blocks.extend(blocks_fn(context))
    else:
        if isinstance(context, RunFailureSensorContext):
            text = (
                f'Dagster Job Failure! \n'
                f'*Job "{context.dagster_run.job_name}" failed.'
                f' `{context.dagster_run.run_id.split("-")[0]}`* \n'
                f'Error: {context.failure_event.message} \n'
            )
        else:
            text = (
                f'*Asset "{context.asset_key.to_user_string()}" is now'
                f' {"on time" if context.minutes_overdue == 0 else f"{context.minutes_overdue:.2f} minutes late.*"}'
            )

        blocks.extend(
            [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text,
                    },
                },
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": main_body_text},
                },
            ]
        )

    if webserver_base_url:
        if isinstance(context, RunFailureSensorContext):
            url = f"{webserver_base_url}/runs/{context.dagster_run.run_id}"
        else:
            url = f"{webserver_base_url}/assets/{'/'.join(context.asset_key.path)}"
        blocks.append(
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View in Dagster UI"},
                        "url": url,
                    }
                ],
            }
        )
    return blocks, main_body_text


dagster_slack.sensors._build_slack_blocks_and_text = custom_build_slack_blocks_and_text


def make_slack_on_failure_sensor() -> SensorDefinition:
    """
    Creates the sensor to trigger on job failures to send messages

    :return: Creates the sensor
    :rtype: SensorDefinition
    """
    return make_slack_on_run_failure_sensor(
        channel="#data-alerts",
        slack_token=os.environ.get("slack_fitness_mds_token", ""),
    )
