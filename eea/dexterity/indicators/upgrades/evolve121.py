"""Upgrade step to update workflow tools for archived state"""
import logging
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.context import SetupEnviron
from Products.GenericSetup.tool import SetupTool

logger = logging.getLogger('eea.dexterity.indicators.upgrades')


def to_121(context):
    """Update workflow tools to ensure archived state is properly recognized"""
    logger.info("Starting workflow tool update for archived state...")
    
    # Get the portal setup tool and re-import workflow definitions
    setup_tool = getToolByName(context, 'portal_setup')
    
    # Re-import the workflow tool to ensure it picks up the archived state
    setup_tool.runImportStepFromProfile(
        'eea.dexterity.indicators:default',
        'workflow',
        run_dependencies=False
    )
    
    # Get the workflow tool
    wf_tool = getToolByName(context, 'portal_workflow')
    
    # Update the IMS indicator workflow specifically
    workflow_id = 'ims_indicator_workflow'
    if workflow_id in wf_tool.objectIds():
        workflow = wf_tool[workflow_id]
        
        # Force refresh of workflow definition from filesystem
        workflow.updateRoleMappingsFor(context)
        
        # Update all role mappings for this workflow
        wf_tool.updateRoleMappings()
        
        logger.info(f"Updated workflow {workflow_id} - archived state should now be available")
        
        # Log available transitions for verification
        if hasattr(workflow, 'transitions'):
            available_transitions = list(workflow.transitions.keys())
            logger.info(f"Available transitions: {available_transitions}")
            if 'archived' in available_transitions:
                logger.info("SUCCESS: archived transition is now available")
            else:
                logger.error("FAILED: archived transition still not available")
    else:
        logger.warning(f"Workflow {workflow_id} not found in workflow tool")
    
    # Clear any cached workflow information
    if hasattr(wf_tool, '_v_wf_cache'):
        delattr(wf_tool, '_v_wf_cache')
    
    # Clear workflow chains cache
    if hasattr(wf_tool, '_chains_by_type'):
        wf_tool._p_changed = True
    
    logger.info("Workflow tool update completed successfully")