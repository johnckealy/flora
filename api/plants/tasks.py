from celery import shared_task
from scripts.thingspeak_integration import run as run_integration
from scripts.sync_to_airtable import run as run_sync
from celery.decorators import task



@task(name="manual_integration")
def manual_integration():
    run_integration()

@shared_task(name="integration")
def run_integration_script():
    run_integration()

@shared_task(name="sync_plants")
def run_sync_script():
    run_sync()
