"""Upgrade step to add new dividers to all indicators"""
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler


def add_dividers_to_indicators(context):
    """Add new dividers 43df8fab-b278-4b0e-a62c-ce6b8e0a881d and 43df8fab-b278-4b0e-a62c-ce6b8e0a881e to all indicators"""
    ctool = getToolByName(context, "portal_catalog")
    brains = ctool.unrestrictedSearchResults(portal_type="ims_indicator")
    pghandler = ZLogHandler(100)
    pghandler.init("Add new dividers to all indicators", len(brains))
    
    # Define the new divider blocks
    new_dividers = {
        "43df8fab-b278-4b0e-a62c-ce6b8e0a881d": {
            "@type": "dividerBlock",
            "section": False,
            "short": True,
            "disableNewBlocks": True,
            "fixed": True,
            "hidden": True,
            "readOnly": True,
            "required": True,
            "styles": {},
            "spacing": "s",
            "fitted": False,
        },
        "43df8fab-b278-4b0e-a62c-ce6b8e0a881e": {
            "@type": "dividerBlock",
            "section": False,
            "short": True,
            "disableNewBlocks": True,
            "fixed": True,
            "hidden": True,
            "readOnly": True,
            "required": True,
            "spacing": "s",
            "fitted": False,
        }
    }
    
    def find_group_by_id_or_title(blocks, group_id, group_title):
        """Find group block by ID first, then by title"""
        # First try to find by ID
        if group_id in blocks:
            return group_id, blocks[group_id]
        
        # If not found by ID, search by title
        for block_id, block_data in blocks.items():
            if isinstance(block_data, dict) and block_data.get("title") == group_title:
                return block_id, block_data
        
        return None, None
    
    for idx, brain in enumerate(brains):
        pghandler.report(idx)
        doc = brain.getObject()
        
        # Check if the document has blocks
        if not hasattr(doc, 'blocks') or not doc.blocks:
            continue
            
        blocks_modified = False
        
        # Find the Aggregate level assessment group and add the first divider
        aggregate_group_id, aggregate_group = find_group_by_id_or_title(
            doc.blocks, 
            "1bc4379d-cddb-4120-84ad-5ab025533b12", 
            "Aggregate level assessment"
        )
        
        if aggregate_group and "data" in aggregate_group and "blocks" in aggregate_group["data"]:
            aggregate_blocks = aggregate_group["data"]["blocks"]
            
            # Add the first divider if it doesn't exist
            if "43df8fab-b278-4b0e-a62c-ce6b8e0a881d" not in aggregate_blocks:
                aggregate_blocks["43df8fab-b278-4b0e-a62c-ce6b8e0a881d"] = new_dividers["43df8fab-b278-4b0e-a62c-ce6b8e0a881d"]
                
                # Add to layout if not present
                if "blocks_layout" in aggregate_group["data"] and "items" in aggregate_group["data"]["blocks_layout"]:
                    layout_items = aggregate_group["data"]["blocks_layout"]["items"]
                    if "43df8fab-b278-4b0e-a62c-ce6b8e0a881d" not in layout_items:
                        # Insert after the embed_content block
                        embed_block_id = "b0279dde-1ceb-4137-a7f1-5ab7b46a782c"
                        if embed_block_id in layout_items:
                            embed_index = layout_items.index(embed_block_id)
                            layout_items.insert(embed_index + 1, "43df8fab-b278-4b0e-a62c-ce6b8e0a881d")
                        else:
                            layout_items.append("43df8fab-b278-4b0e-a62c-ce6b8e0a881d")
                
                blocks_modified = True
        
        # Find the Disaggregate level assessment group and add the second divider
        disaggregate_group_id, disaggregate_group = find_group_by_id_or_title(
            doc.blocks,
            "d060487d-88fc-4f7b-8ea4-003f14e0fb0c",
            "Disaggregate level assessment"
        )
        
        if disaggregate_group and "data" in disaggregate_group and "blocks" in disaggregate_group["data"]:
            disaggregate_blocks = disaggregate_group["data"]["blocks"]
            
            # Add the second divider if it doesn't exist
            if "43df8fab-b278-4b0e-a62c-ce6b8e0a881e" not in disaggregate_blocks:
                disaggregate_blocks["43df8fab-b278-4b0e-a62c-ce6b8e0a881e"] = new_dividers["43df8fab-b278-4b0e-a62c-ce6b8e0a881e"]
                
                # Add to layout if not present
                if "blocks_layout" in disaggregate_group["data"] and "items" in disaggregate_group["data"]["blocks_layout"]:
                    layout_items = disaggregate_group["data"]["blocks_layout"]["items"]
                    if "43df8fab-b278-4b0e-a62c-ce6b8e0a881e" not in layout_items:
                        # Insert after the embed_content block
                        embed_block_id = "02ba4a04-fcfe-4968-806f-1dac3119cfef"
                        if embed_block_id in layout_items:
                            embed_index = layout_items.index(embed_block_id)
                            layout_items.insert(embed_index + 1, "43df8fab-b278-4b0e-a62c-ce6b8e0a881e")
                        else:
                            layout_items.append("43df8fab-b278-4b0e-a62c-ce6b8e0a881e")
                
                blocks_modified = True
        
        if blocks_modified:
            doc.reindexObject()
            
    pghandler.finish()